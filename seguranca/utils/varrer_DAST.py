import requests, logging, json, paramiko, subprocess, os 

from django.utils import timezone

from seguranca.serializers import ResultadoScanSerializer
#from seguranca.utils import varredura_result
from celery import shared_task


#headears = {'Authorization':'Token 61a384f801cb080e0c8f975c7731443b51c9f02e'}
headers = {'Content-Type': 'application/json'}
#url_base = "http://192.168.0.22:8000/api/v2"
#url_base_aplicacoes = f"{url_base}/aplicacoes/"
url_api = os.getenv('URL_API')
url_base_aplicacoes = f'{url_api}/v2/aplicacoes/'

logger = logging.getLogger(__name__)  

work_path = '/zap/wrk'
report_path = '/zap/wrk/reports'
report_name = "owasp_zap_report_{aplicacao}.json"

jsondoc = {
      "erros": 0, 
      "falhas": 0, 
      "testes": 0, 
      "tempo": 0
    }

# define a conexão SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
# realiza o processamento da varredura
@shared_task(soft_time_limit=600, time_limit=600) #limitar em 10 minutos o processamento
def processa (processar):
  """
  Inicializar as variáveis de ambiente
  Recebe os dados passados através de um JSON para processar a varredura da aplicação
  processar = {
    "aplicacao": aplicacao.nome,
    "aplicacao_sigla": aplicacao.sigla,     
    "aplicacao_id": aplicacao.id,
    "url_codigo_fonte": aplicacao.url_codigo_fonte,
    "varredura": serializer.data['id'],
    "sistema_varredura": sist_varr.id,
    "sist_varredura_ip_acesso": sist_varr.ip_acesso,
    "sist_varredura_host": sist_varr.aplicacao_seguranca.url_codigo_fonte,
    "sist_varredura_comando": sist_varr.comando,
    "sist_varredura_webhook": sist_varr.usa_webhook,
    "sist_varredura_tipo": sist_varr.tipo_varredura,
    "sist_varredura_sigla_tipo": "SAST",
    "sist_varredura_usuario": sist_varr.usuario,
    "sist_varredura_senha": sist_varr.senha,
    "sist_varredura_token": sist_varr.token_acesso,
    "caminho_resultado": f"{aplicacao.sigla}_{sist_varredura.sigla}_{datetime.now().strftime('%Y%m%d%H%M%S")}.json"
  }
  """
  #print()
  #print (processar)
  #print()
  # 1º passo: criar o script de autenticação para a aplicação com usuário e senha
  script_js = """function authenticate(helper, paramsValues, credentials) {
        print("Authenticating via JavaScript script...");
        // Make sure any Java classes used explicitly are imported
        var HttpRequestHeader = Java.type("org.parosproxy.paros.network.HttpRequestHeader")
        var HttpHeader = Java.type("org.parosproxy.paros.network.HttpHeader")
        var URI = Java.type("org.apache.commons.httpclient.URI")
        
        // Prepare the login request details
        var requestUri = new URI(paramsValues.get("Target URL"), false);
        var requestMethod = HttpRequestHeader.POST;
	
	    // Build the request body using the credentials values
        var extraPostData = paramsValues.get("Extra POST data");
        var requestBody = paramsValues.get("Username field") + "=" + encodeURIComponent(credentials.getParam("Username"));
        requestBody+= "&" + paramsValues.get("Password field") + "=" + encodeURIComponent(credentials.getParam("Password"));
        
        if(extraPostData.trim().length() > 0)
            requestBody += "&" + extraPostData.trim();

    	// Build the actual message to be sent
        print("Sending " + requestMethod + " request to " + requestUri + " with body: " + requestBody);
        var msg = helper.prepareMessage();
        msg.setRequestHeader(new HttpRequestHeader(requestMethod, requestUri, HttpHeader.HTTP10));
        msg.setRequestBody(requestBody);
        msg.getRequestHeader().setContentLength(msg.getRequestBody().length());

    	// Send the authentication message and return it
        helper.sendAndReceive(msg);
        print("Received response status code: " + msg.getResponseHeader().getStatusCode());

	    return msg;
    }
    
    function getRequiredParamsNames(){
        return ["Target URL", "Username field", "Password field"];
    }

    function getOptionalParamsNames(){
        return ["Extra POST data"];
    }

    function getCredentialsParamsNames(){
        return ["Username", "Password"];
    }
  """
  # 1º Passo: Transfere o arquivo para o servidor remoto
  try:
    ssh.connect(hostname=processar["sist_varredura_ip_acesso"], username=processar["sist_varredura_usuario"], password=processar["sist_varredura_senha"])
    # 2º passo: rodar o scanner do owasp-zap via CLI
    #comando = f"docker exec mn.owasp_zap bash -c 'zap.sh -dir wrk -loglevel ERROR -script wrk/scripts/authentication.js -cmd -quickurl {url_zap} -quickprogress -quickout {output}'\n"
    #comando = f"docker exec mn.owasp_zap bash -c 'python zap-full-scan.py -t {url_zap} -J {output} -d'\n"
    #comando = f"docker exec mn.owasp_zap bash -c '{processar['sist_varredura_comando']}'\n"
    comando = f"{processar['sist_varredura_comando']}"
    #python zap-full-scan.py -t  {url_zap} -J {pasta}/owasp_zap_report_{aplicacao}.json -d
    cmd = comando.replace( "{aplicacao}", processar["aplicacao_sigla"].lower())
    cmd = cmd.replace( "{url_zap}", processar["sist_varredura_host"])
    cmd = cmd.replace( "{pasta}", "reports")
    print (f"1º passo: Comando: {cmd}")
    try:
      logger.info (f"Iniciando a análise de vulnerabilidade da aplicação {processar['aplicacao_sigla']}...")
      stdin,stdout,stderr = ssh.exec_command(cmd)
      cod_erro = stderr.channel.recv_exit_status()
      saida = stdout.readlines()
      erro = stderr.readlines()
      if cod_erro == 0:
        print(f"Análise da aplicação {processar['aplicacao_sigla']} realizada com sucesso!")
        logger.info (f"Análise da aplicação {processar['aplicacao_sigla']} realizada com sucesso!")
        #2º passo: carregar o resultado da varredura
        #comando = f"docker exec mn.owasp_zap cat /wrk/{output}"
        #report_path = 'zap/wrk'
        #report_name = "owasp_zap_report_{aplicacao}.json"
        #comando = f"docker exec mn.owasp_zap cat /src/report/<aplicacao>/dependency-check-report.json"
        arquivo_report = report_name.replace('{aplicacao}',processar['aplicacao_sigla'].lower())
        #comando = f"docker exec mn.owasp_zap cat {report_path}/{arquivo}"
        comando = f"cat {report_path}/{arquivo_report}"
        print(f"2º passo: Comando: {comando}")
        try:
          #baixar o arquivo de resultado da varredura para a máquina remota do docker
          stdin,stdout,stderr = ssh.exec_command(comando) 
          cod_erro = stderr.channel.recv_exit_status()
          saida = stdout.readlines()
          erro = stderr.readlines()
          if cod_erro == 0:
            # copiar o arquivo localmente para a pasta midia
            arq_origem = arquivo_report
            arq_destino = f"midia/{arquivo_report}"
            # copia o arquivo para pasta local
            with open(arq_destino, 'w') as arquivo:
              dados = json.dump(saida.replace("\\','").replace("[\"','").replace("\"]','"), arquivo,indent=3)
              print("Arquivo de resultado carregado com sucesso!")  
              print (dados)
              string_resultado={
                "data_resultado": timezone.now(),
                "resultado": json.dumps(dados,indent=3),
                "aplicacao": processar["aplicacao_id"],
                "varredura": processar["varredura"],      
                "sistema_varredura": processar["sistema_varredura"]
              }
              serializer =  ResultadoScanSerializer(data=string_resultado)
              if serializer.is_valid():
                serializer.save()
                print(f"Resultado salvo com sucesso: {serializer.data}")
                return requests.Response(serializer.data, status=201)
              else:
                print(f"Erro ao salvar o resultado: {serializer.errors}")
                return requests.Response(serializer.errors, status=400)
                jsondoc["erros"] = 1
          else: 
            print(f"Erro ao tentar copiar os dados do resultado da varredura")
            logger.error (f"Erro ao tentar copiar os dados do resultado da varredura")
            jsondoc["erros"] = 1    
        except paramiko.SSHException as e2:
          print(f"Erro ao tentar copiar o resultada da análise:\n {e2}")
          logger.error (f"Erro ao tentar copiar o resultada da análise:\n {e2}")
          jsondoc["erros"] = 1
      else:
        print(f"Erro ao analisar a aplicação")
        logger.error (f"Erro ao analisar a aplicação")    
        jsondoc["erros"] = 1
    except paramiko.SSHException as e3:
      print(f"Erro ao executar o comando remoto para análise da vulnerabilidades:\n {e3}")
      logger.error (f"Erro ao executar o comando remoto para análise da vulnerabilidades:\n {e3}")
      jsondoc["erros"] = 1
  except paramiko.SSHException as e4:
      print(f"Erro ao tentar conectar no servidor remoto:\n {e4}")
      logger.error (f"Erro ao tentar conctar no servidor remoto:\n {e4}")
      jsondoc["erros"] = 1
  finally:
    ssh.close()    
    # retornar o resultado
    resultado = {
      "aplicacao": processar["aplicacao_id"],
      "varredura": processar["varredura"],
      "sistemas_varredura": processar["sistema_varredura"],
      "resultado": jsondoc,
    }   
    return (resultado)

         
 
  
  
    # 1º passo: criar e copiar arquivo de configuração para o servidor Owasp_ZAP
    # Cria um objeto para armazenar o conteúdo do arquivo
    #sftp = ssh.open_sftp()
    # Se o conteúdo for fornecido, cria um arquivo em memória
    #script = f"midia/authentication.js"
    #print (f"Script: {script}")
    #if script_js:
    #  #print ("Criando o arquivo... ",script_js)
    #  try: 
    #    with open(script, 'w') as arquivo:
    #      arquivo.write (script_js)
    #    #arquivo = io.BytesIO(script_js.encode('utf-8'))
    #    print ("Arquivo criado com sucesso!")
    #  except IOError as eee:
    #    print(f'Erro ao criar o arquivo remoto: {eee}')
    #    logger.error (f'Erro ao criar o arquivo remoto: {eee}')
    
    #try:  
      #sftp.putfo(arquivo, "authentication.js")
      #comando = f"docker cp authentication.js mn.owasp_zap:/zap/wrk/scripts/authentication.js\n"
      #ssh.connect(hostname=processar["sist_varredura_ip_acesso"], username=processar["sist_varredura_usuario"], password=processar["sist_varredura_senha"])
      #comando = f"scp {script} {processar['sist_varredura_usuario']}@{processar['sist_varredura_ip_acesso']}:{work_path}/scripts/authentication.js\n"
      #print()
      #print (f"1º Passo: {comando}")
      #try:
      #  subprocess.run(comando, shell=True,check=True)
        # processar arquivo de resultado
      #except subprocess.CalledProcessError as e2:
      #  print(f"Erro ao copiar o arquivo de resultado: {e}")
      #  logger.error (f"Erro ao copiar o arquivo de resultado: {e}") 
      #     stdin,stdout,stderr = ssh.exec_command(comando)
      #     stdin.write('docker\n')
      #     stdin.flush()    
      #     stdin.close()
      #     #print(f"stdout: {stdout.readlines()}")
      #     #print(f"stderr: {stderr.readlines()}")  
      # except ssh.exec_command as e2:
      #     print(f'Erro ao criar o arquivo remoto: {e2}')
      #     logger.error (f'Erro ao criar o arquivo remoto: {e2}')
    #except paramiko.SSHException as e1:
    #  print(f'Erro ao criar o arquivo remoto: {e1}')
    #  logger.error (f'Erro ao criar o arquivo remoto: {e1}')
  # except paramiko.SSHException as e:
  #   print(f'Erro ao criar o arquivo remoto: {e}')
  #   logger.error (f'Erro ao criar o arquivo remoto: {e}')
  
  # # 2º passo: rodar o scanner do owasp-zap via CLI
  # #comando = f"docker exec mn.owasp_zap bash -c 'zap.sh -dir wrk -loglevel ERROR -script wrk/scripts/authentication.js -cmd -quickurl {url_zap} -quickprogress -quickout {output}'\n"
  # #comando = f"docker exec mn.owasp_zap bash -c 'python zap-full-scan.py -t {url_zap} -J {output} -d'\n"
  # #comando = f"docker exec mn.owasp_zap bash -c '{processar['sist_varredura_comando']}'\n"
  # comando = f"{processar['sist_varredura_comando']}"
  # cmd = comando.replace( "{aplicacao}", processar["aplicacao_sigla"].lower())
  # cmd = cmd.replace( "{url_zap}", processar["sist_varredura_host"])
  # cmd = cmd.replace( "{pasta}", "reports")
  # print()
  # print (f"2º passo: Comando: {cmd}")
  # try:
  #     logger.info (f"Iniciando a análise de vulnerabilidade da aplicação {processar['aplicacao_sigla']}...")
  #     stdin,stdout,stderr = ssh.exec_command(cmd)
  #     stdin.write("docker\n")
  #     stdin.flush()    
  #     stdin.close()
  #     #print(f"stdout: {stdout.readlines()}")
  #     #print(f"stderr: {stderr.readlines()}")    
  #     print(f"Status: {stderr.channel.recv_exit_status()}")
  #     logger.info (f"Status: {stderr.channel.recv_exit_status()}")
  #     #if stderr.channel.recv_exit_status() == 0:
  #     if stderr.readlines() == []:
  #         #print("Análise realizada com sucesso!")
  #         logger.info (f"Análise da aplicação " + processar["aplicacao_sigla"] + "realizada com sucesso.")
  #     else:
  #         print (f"Erro ao executar a varredura. stderr: {stderr.readlines()}; stdout: {stdout.readlines()}")
  #         logger.error (f"Erro ao executar a varredura: stderr: {stderr.readlines()}; stdout: {stdout.readlines()}")
  # except paramiko.SSHException as e:
  #     print(f"Erro ao executar o comando remoto: {e}")
  #     logger.error (f"Erro ao executar o comando remoto: {e}")
  
  # #3º passo: carregar o resultado da varredura
  # #comando = f"docker exec mn.owasp_zap cat /wrk/{output}"
  # #report_path = 'zap/wrk'
  # #report_name = "owasp_zap_report_{aplicacao}.json"
  # #comando = f"docker exec mn.owasp_zap cat /src/report/<aplicacao>/dependency-check-report.json"
  # arquivo_report = report_name.replace('{aplicacao}',processar['aplicacao_sigla'].lower())
  # comando = f"docker exec mn.owasp_zap cat {report_path}/{arquivo}"
  # print()
  # print(f"3º passo: Comando: {comando}")
  # try:
  #   #baixar o arquivo de resultado da varredura para a máquina remota do docker
  #   cmd = f"docker cp mn.owasp_zap:{report_path}/{arquivo_report} {arquivo_report}"
  #   stdin,stdout,stderr = ssh.exec_command(cmd) 
  #   stdin.write("docker\n")
  #   stdin.flush()
  #   stdin.close()
  #   # copiar o arquivo localmente para a pasta midia
  #   arq_origem = arquivo_report
  #   arq_destino = f"midia/{arquivo_report}"
  #   cmd = f"scp {processar['sist_varredura_usuario']}@{processar['sist_varredura_ip_acesso']}:{arq_origem} {arq_destino}" 
  #   # copia o arquivo para pasta local
  #   try:
  #     subprocess.run(cmd, shell=True,check=True)
  #     # processar arquivo de resultado
  #     with open(arq_destino, 'r') as arquivo:
  #       dados = json.load(arquivo)
  #     # trocando caracteres inválidos
  #     for chave, valor in dados.items():
  #         if isinstance(valor, str):
  #             dados[chave] = valor.replace('\\', '').replace('["', '').replace('"]', '')
  #     #salvando o arquivo de resultado
  #     arq_destino = f"midia/novo_{arq_origem}"
  #     try:
  #       with open(arq_destino, 'w') as arquivo:
  #         dados = json.dump(dados, arquivo,indent=3)
  #         #print("Arquivo de resultado carregado com sucesso!")  
  #         #payload = json.dumps(dados,indent=3)
  #       try:
  #           with open(arq_destino, 'r') as arquivo:
  #             dados = json.load(arquivo)
  #           #print (f"Resultado da varredura: {dados}")
  #           string_resultado={
  #               "data_resultado": timezone.now(),
  #               "resultado": json.dumps(dados,indent=3),
  #               "aplicacao": processar["aplicacao_id"],
  #               "varredura": processar["varredura"],      
  #               "sistema_varredura": processar["sistema_varredura"]
  #               }
  #           #print()
  #           #print(data)
  #           print("Passou aqui...")
  #           # gravando o resultado na base de dados
  #           #resultado = varredura_result.processa_resultado(request.data)
  #           # validar o serializer e salvar dados no BD
  #           serializer =  ResultadoScanSerializer(data=string_resultado)
  #           if serializer.is_valid():
  #             serializer.save()
  #             print(f"Resultado salvo com sucesso: {serializer.data}")
  #             return requests.Response(serializer.data, status=201)
  #           else:
  #             print(f"Erro ao salvar o resultado: {serializer.errors}")
  #             return requests.Response(serializer.errors, status=400)
            
  #           #response = requests.post('http://192.168.0.22:8000/api/v1/resultados/',data=dados, headers=headers)
  #       except requests.exceptions.RequestException as e:
  #           print(f"Erro ao enviar os dados para gravação no BD: {e} ")
  #           logger.error (f"Erro ao salvar os dados no BD: {e}")
  #       print()
  #     except Exception as e:
  #       print(f"Erro ao salvar o arquivo de resultado: {e}")
  #       logger.error (f"Erro ao salvar o arquivo de resultado: {e}")
  #   except subprocess.CalledProcessError as e:
  #     print(f"Erro ao copiar o arquivo de resultado: {e}")
  #     logger.error (f"Erro ao copiar o arquivo de resultado: {e}")
    
  # except paramiko.SSHException as e:
  #   print(f"Erro ao executar o comando remoto: {e}")
  #   logger.error (f"Erro ao executar o comando remoto: {e}")

  # # finalizar processamento
  # ssh.close()
  
  
  # # retornar o resultado
  # resultado = {
  #   "aplicacao": processar["aplicacao_id"],
  #   "varredura": processar["varredura"],
  #   "sistemas_varredura": processar["sistema_varredura"],
  #   "resultado": jsondoc,
  # }   
  # return (resultado)

         
