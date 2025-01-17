import requests, logging, json, paramiko, paramiko.message, os

#from . import mod_ssh

from celery import shared_task

#headears = {'Authorization':'Token 61a384f801cb080e0c8f975c7731443b51c9f02e'}
headers = {'Content-Type': 'application/json'}
url_api = os.getenv('URL_API')
url_base_aplicacoes = f'{url_api}/v2/aplicacoes/'

logger = logging.getLogger(__name__)  

jsondoc = {
      "erros": 0, 
      "falhas": 0, 
      "testes": 0, 
      "tempo": 0
    }

# define a conexão SSH que vai ser utilizada 
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#ssh.load_system_host_keys()
    
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
  #print (processar["sist_varredura_ip_acesso"], processar["sist_varredura_usuario"], processar["sist_varredura_senha"],"\n")
  try:
    # Conecta via SSH no host para processamenteo da varredura
    print ('Conectando  via SSH...')
    ssh.connect(hostname=processar["sist_varredura_ip_acesso"], username=processar["sist_varredura_usuario"], password=processar["sist_varredura_senha"])
    # clonar o repositório da aplicação a ser analisada
    comando = f"rm -rf /tmp/{processar['aplicacao_sigla'].lower()} && cd /tmp && git clone {processar['url_codigo_fonte']}"
    comando = f"{comando} && mv -f {processar['aplicacao_sigla']} {processar['aplicacao_sigla'].lower()}"
    # adapatacao feita no TRT21 para copiar usando git (ssh) ao inves de https
    comando = comando.replace("https://git.trt21.local/","git@git.trt21.local:")
    print (f"Clonando o repositório... {comando}")
    stdin,stdout,stderr = ssh.exec_command(comando)
    cod_erro = stderr.channel.recv_exit_status()
    erro = stderr.readlines()
    saida = stdout.readlines()
    if  cod_erro == 0:
      print(f"Clonagem da aplicação {processar['aplicacao_sigla']} realizada com sucesso!")
      logger.info (f"Clonagem da aplicação {processar['aplicacao_sigla']} realizada com sucesso!")
      # obtem o camando de varredura a ser executado pela ferramenta de varredura de vulnerabiliade
      comando = processar["sist_varredura_comando"] 
      try:
        # pega a aplicação para obter os dados para processamento
        #print(f"{url_base_aplicacoes}{processar['sistema_varredura']}")
        response = requests.get (f"{url_base_aplicacoes}{processar['sistema_varredura']}")
        response.raise_for_status()
        # pega os dados da aplicação
        app_url_acesso = processar["sist_varredura_url_acesso"] #response.json().get('url_codigo_fonte')
        app_usuario_servico = processar["sist_varredura_usr_servico"]   #response.json().get('usuario_servico')
        app_senha_servico = processar["sist_varredura_senha_servico"]   #os.getenv('SENHA_SERVICO') 
        app_token_acesso = processar["sist_varredura_token_servico"]
        try:
          # substitui os dados do comando pelos obtidos da aplicação
          cmd = comando.replace("{aplicacao}", processar["aplicacao_sigla"].lower())
          cmd = cmd.replace("https://git.trt21.local/","git@git.trt21.local:")
          cmd = cmd.replace("{app_host}", app_url_acesso)
          cmd = cmd.replace("{app_token}", app_token_acesso)
          cmd = cmd.replace("{user}", app_usuario_servico)
          cmd = cmd.replace("{password}", app_senha_servico)
          print (f"Varrendo vulnerabilidades... {cmd}\n")
        except Exception as ex:
          print (f"Erro ao substituir dados do comando:\n{ee}")
          logger.error (f"Erro ao substituir dados do comando:\n {ex}")
          jsondoc["erros"] = 1
          jsondoc["mensagem"] = ex
        try:
          stdin,stdout,stderr = ssh.exec_command(cmd)
          cod_erro = stderr.channel.recv_exit_status()
          erro = stderr.readlines()
          saida = stdout.readlines()
          if cod_erro == 0:
            print(f"Análise da aplicação {processar['aplicacao_sigla']} realizada com sucesso!")
            logger.info (f"Análise da aplicação {processar['aplicacao_sigla']} realizada com sucesso!")
            if not processar["sist_varredura_webhook"]:  #se usar webhook o carregamento é feito pela chamado do webhook
               print(f"3º passo: Comando: {processar['caminho_resultado']}")
               carregar_arquivo_resultado (processar)
               # finalizar processamento
            ssh.close()
            # retornar o resultado
            resultado = {
              "aplicacao": processar["aplicacao_id"],
              "varredura": processar["varredura"],
              "sistemas_varredura": processar["sistema_varredura"],
              "resultado": jsondoc,
            }
            #print (resultado)
            return (resultado)
          else:
            print (f"Erro ao validar vulnerabilidades do repositório:\n {erro}")
            logger.error (f"Erro ao validar vulnerabilidades do repositório:\n {erro}")
            jsondoc["erros"] = 1
            jsondoc["mensagem"] = erro
        except paramiko.SSHException as e1:
          print(f'Erro ao executar o comando remoto {comando}:\n {e1}')
          logger.error(f'Erro ao executar o comando remoto {comando}:\n {e1}')
          jsondoc["erros"] = 1
          jsondoc["mensagem"] = e1
      except requests.exceptions.HTTPError as e2:
        print (f"Erro ao buscar os dados da aplicação:\nErro {response.status_code}\n{e2}")
        logger.error (f"Erro ao buscar os dados da aplicação:\nErro {response.status_code}\n{e2}")
        jsondoc["erros"] = 1
        jsondoc["mensagem"] = e2
    else:
      print (f"Erro ao clonar o repositório:\n {erro}")
      logger.error (f"Erro ao clonar o repositório:\n {erro}")
      jsondoc["erros"] = 1
      jsondoc["mensagem"] = erro
  except paramiko.SSHException as e3:
    print(f'Erro ao executar o comando remoto {comando}:\n {e3}')
    logger.error(f'Erro ao executar o comando remoto {comando}:\n {e3}')
    jsondoc["erros"] = 1
    jsondoc["mensagem"] = e3
  finally:
    resultado = {
      "aplicacao": processar["aplicacao_id"],
      "varredura": processar["varredura"],
      "sistemas_varredura": processar["sistema_varredura"],
      "resultado": jsondoc,
    }
    ssh.close()
    return (resultado)
  
  
  
  
  # try: 
  #   subprocess.call (comando,shell=True)
  #   if os.path.exists(f"/tmp/{processar['aplicacao_sigla'].lower()}"):
  #     print (f"Clonagem da aplicação {processar['aplicacao_sigla']} realizada com sucesso.")
  #     # copiar o arquivo para o servidor remoto
  #     #comando = f"scp -r /tmp/{processar['aplicacao_sigla'].lower()} {processar['sist_varredura_usuario']}:{processar['sist_varredura_senha']}@"
  #     comando = f"scp -r /tmp/{processar['aplicacao_sigla'].lower()} {processar['sist_varredura_usuario']}@"
  #     comando = f"{comando}{processar['sist_varredura_ip_acesso']}:/tmp"
  #     print (f"Copiando arquivo: Comando: {comando}")
  #     subprocess.call (comando,shell=True)
  #     # conectar no servidor remoto
  #     #print (f"hostname={processar['sist_varredura_ip_acesso']}", f"username={processar['sist_varredura_usuario']}", f"password={processar['sist_varredura_senha']}")
  #     try:  
  #       keyfile = '/home/root/.ssh/id_rsa'
  #       ssh.connect(hostname=processar["sist_varredura_ip_acesso"], username=processar["sist_varredura_usuario"], password=processar["sist_varredura_senha"])  
  #       #ssh.connect(hostname=processar["sist_varredura_ip_acesso"], username=processar["sist_varredura_usuario"], key_filename=keyfile)  
  #       # copiar o arquivo por sftp
  #       #sftp = ssh.open_sftp()
  #       #sftp.put(f"/tmp/{processar['aplicacao_sigla'].lower()}", f"/tmp/{processar['aplicacao_sigla'].lower()}")
  #       comando = processar["sist_varredura_comando"] 
  #       try:
  #         response = requests.get (f"{url_base_aplicacoes}{processar['sistema_varredura']}")
  #         app_host = ""
  #         app_usuario_servico=""  
  #         # Senha a ser cadastrada como ENV para o sonarqube e outros serviços associados, com a senha do usuário "servico"
  #         senha_servico=os.getenv('SENHA_SERVICO')
  #         if response.status_code == 200:
  #             app_usuario_servico = response.json().get('usuario_servico')
  #             app_host = response.json().get('url_codigo_fonte')
  #         #print (f"Usuário do serviço: {app_usuario_servico}")
  #         cmd = comando.replace("{aplicacao}", processar["aplicacao_sigla"].lower())
  #         #cmd = cmd.replace("{app_host}", processar["sist_varredura_host"])
  #         cmd = cmd.replace("{app_host}", app_host)
  #         cmd = cmd.replace("{app_token}", processar["sist_varredura_token"])
  #         cmd = cmd.replace("{user}", app_usuario_servico) #processar["sist_varredura_usuario"])  
  #         cmd = cmd.replace("{password}", senha_servico)  #processar["sist_varredura_senha"])  
  #         print (f"2º passo: Comando: {cmd}")
  #         try:
  #           stdin,stdout,stderr = ssh.exec_command(cmd)
  #           stdin.write("docker\n")
  #           stdin.flush()    
  #           stdin.close()
  #           if stderr.channel.recv_exit_status() == 0:
  #             print("Análise realizada com sucesso!")
  #             logger.info (f"Análise da aplicação " + processar["aplicacao_sigla"] + "realizada com sucesso.")
  #             if not processar["sist_varredura_webhook"]:  #se usar webhook o carregamento é feito pela chamado do webhook
  #               print(f"3º passo: Comando: {processar['caminho_resultado']}")
  #               carregar_arquivo_resultado (processar)
  #               # finalizar processamento
  #             ssh.close()
  #             # retornar o resultado
  #             resultado = {
  #               "aplicacao": processar["aplicacao_id"],
  #               "varredura": processar["varredura"],
  #               "sistemas_varredura": processar["sistema_varredura"],
  #               "resultado": jsondoc,
  #             }   
  #             print (resultado)
  #             return (resultado)  
  #           else:
  #             print (f"Erro ao executar a varredura. {stderr.readlines()}")
  #             logger.error (f"Erro ao executar a varredura: {stderr.readlines()}")
  #             jsondoc["erros"] = 1
  #         except paramiko.SSHException as e:
  #             print(f"Erro ao executar o comando remoto: {e}")
  #             logger.error (f"Erro ao executar o comando remoto: {e}")
  #             jsondoc["erros"] = 1
  #       except requests.exceptions.RequestException as e:
  #         print (f"Erro ao buscar os dados da aplicação: {e}")
  #         logger.error (f"Erro ao buscar os dados da aplicação: {e}")       
  #         jsondoc["erros"] = 1
  #     except Exception as e:
  #       print (f"Erro ao copiar o arquivo para o servidor remoto: {e}")
  #       logger.error (f"Erro ao copiar o arquivo para o servidor remoto: {e}")  
  #       jsondoc["erros"] = 1
  #   else:
  #     print (f"Erro ao clonar o repositório da aplicação.")
  #     logger.error (f"Erro ao clonar o repositório da aplicação.")
  #     jsondoc["erros"] = 1
  # except Exception as e:
  #   print (f"Erro ao executar o comando: {e}")
  #   logger.error (f"Erro ao executar o comando: {e}")
  #   jsondoc["erros"] = 1
  # finally:
  #   resultado = {
  #     "aplicacao": processar["aplicacao_id"],
  #     "varredura": processar["varredura"],
  #     "sistemas_varredura": processar["sistema_varredura"],
  #     "resultado": jsondoc,
  #   }   
  #   return (resultado)  

  
  
  #try:
    # baixar o código fonte da aplicação
    #ssh.connect(hostname='192.168.0.10', username='docker', password='docker")
    #ssh.connect(hostname=processar["sist_varredura_ip_acesso"], username=processar["sist_varredura_usuario"], password=processar["sist_varredura_senha"])
    # 1º passo: clonar na máquina do Sonar_CLI a imagem da aplicação a ser varrida
    #comando = f"docker exec mn.sonar_cli bash -c 'cd app && rm -rf DVWA && git clone {dvwa_fonte}'\n"
    # deve rodar o comando na máquina do sonar_cli na pasta app
    #comando = f"docker exec mn.sonar_cli bash -c 'cd app && rm -rf " + processar["aplicacao_sigla"].lower() + " && git clone " + processar["url_codigo_fonte"] + "'\n" # " && mv " + processar["aplicacao_sigla"] + " " + processar["aplicacao_sigla"].lower() + "'\n"
    #comando = f"rm -rf " + processar["aplicacao_sigla"].lower() + " && git clone " + processar["url_codigo_fonte"] + "\n" 
    #comando = f"rm -rf {processar['aplicacao_sigla'].lower()} && git clone {processar['url_codigo_fonte']}"
    #print (f"1º passo: Comando: {comando}")   
    #comando = "ls -lah"
    ### comentado para testar a varredura com dados locais - desabilitar para homologação     
    #try:  
    #    stdin,stdout,stderr = ssh.exec_command(comando)
    #    stdin.write("docker\n")
    #     stdin.flush()    
    #     stdin.close()
    #     # testar se retornou erro
    #     #if stderr.channel.recv_exit_status() == 0:
    #     # if stderr.readlines() != "[]":
    #     #     print("Clonagem realizada com sucesso!")
    #     #     logger.info (f"Clonagem da aplicação " + processar["aplicacao_sigla"] + "realizada com sucesso.")
    #     #     if stderr.channel.recv_exit_status() == 0:
    #     if stderr.channel.recv_exit_status() == 0:        
    #         logger.info (f"Clonagem da aplicação " + processar["aplicacao_sigla"] + "realizada com sucesso.")
    #     else:
    #         #print ("Erro ao clonar o repositório da aplicação.")
    #         logger.error (f"Erro ao clonar o repositório da aplicação: {stderr.readlines()}")
    # except  paramiko.SSHException as e:
    #     print(f"Erro ao executar o comando remoto: {e}")
    #     logger.error (f"Erro ao executar o comando remoto: {e}")  
        
    # 2º passo: executar a varredura da aplicação
    #comando = "sonar-scanner -X -Dsonar.projectKey={aplicacao} -Dsonar.sources=app/{aplicacao} -Dsonar.host.url={app_host} -Dsonar.token={app_token} -Dsonar.login={user} -Dsonar.password={password}"
    #comando = "docker exec mn.sonar_cli bash -c '" + processar["sist_varredura_comando"] + "'" 
    #comando = processar["sist_varredura_comando"] 
    #response = requests.get (f"{url_base_aplicacoes}{processar['sistema_varredura']}")
    #print(response.json())
    # app_host = ""
    # app_usuario_servico=""  
    # # Senha a ser cadastrada como ENV para o sonarqube e outros serviços associados, com a senha do usuário "servico"
    # senha_servico=os.getenv('SENHA_SERVICO')
    # if response.status_code == 200:
    #     app_usuario_servico = response.json().get('usuario_servico')
    #     app_host = response.json().get('url_codigo_fonte')
    # #print (f"Usuário do serviço: {app_usuario_servico}")
    # cmd = comando.replace("{aplicacao}", processar["aplicacao_sigla"].lower())
    # #cmd = cmd.replace("{app_host}", processar["sist_varredura_host"])
    # cmd = cmd.replace("{app_host}", app_host)
    # cmd = cmd.replace("{app_token}", processar["sist_varredura_token"])
    # cmd = cmd.replace("{user}", app_usuario_servico) #processar["sist_varredura_usuario"])  
    # cmd = cmd.replace("{password}", senha_servico)  #processar["sist_varredura_senha"])  
    # print (f"2º passo: Comando: {cmd}")
    # try:
    #     stdin,stdout,stderr = ssh.exec_command(cmd)
    #     stdin.write("docker\n")
    #     stdin.flush()    
    #     stdin.close()
    #     if stderr.channel.recv_exit_status() == 0:
    #         print("Análise realizada com sucesso!")
    #         logger.info (f"Análise da aplicação " + processar["aplicacao_sigla"] + "realizada com sucesso.")
    #     else:
    #         print (f"Erro ao executar a varredura. {stderr.readlines()}")
    #         logger.error (f"Erro ao executar a varredura: {stderr.readlines()}")
    # except paramiko.SSHException as e:
    #     print(f"Erro ao executar o comando remoto: {e}")
    #     logger.error (f"Erro ao executar o comando remoto: {e}")
    
    #3º passo: carregar o resultado da varredura
  #   if not processar["sist_varredura_webhook"]:  #se usar webhook o carregamento é feito pela chamado do webhook
  #     carregar_arquivo_resultado (processar)
  #   # finalizar processamento
  #   ssh.close()
    
  #   # retornar o resultado
  #   resultado = {
  #     "aplicacao": processar["aplicacao_id"],
  #     "varredura": processar["varredura"],
  #     "sistemas_varredura": processar["sistema_varredura"],
  #     "resultado": jsondoc,
  #   }   
  #   print (resultado)
  #   return (resultado)
  
  # except paramiko.SSHException as e:    
  #   print(f"Erro ao conectar ao servidor remoto: {e}")
  #   logger.error (f"Erro ao conectar ao servidor remoto: {e}")

def carregar_arquivo_resultado (processar):
  #comando = "docker exec mn.owasp_dc cat /src/report/dependency-check-report.json"
  #comando = "docker exec mn.sonar_cli cat " + processar["caminho_resultado"]
  comando = "cat " + processar["caminho_resultado"]
  cmd = comando.replace( '{aplicacao}', processar["aplicacao_sigla"])  
  print(f"3º passo: Comando: {cmd}")
  try:
    stdin,stdout,stderr = ssh.exec_command(cmd)
    stdin.write("docker\n")
    stdin.flush()    
    stdin.close()
    # testar se retornou erro
    if stderr.channel.recv_exit_status() == 0:
        print("Análise realizada com sucesso!")
        data = json.dumps(stdout.readlines())
        dados = json.loads(data.replace("\\','").replace("[\"','").replace("\"]','"))
        print ("------------------------------------")
        payload = json.dumps(dados,indent=3)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{url_api}/v1/resultados/',data=payload, headers=headers)
        if response.status_code == 201:
            print("Dados inseridos no BD!")
            logger.info (f"Resultado da análise "+ processar["aplicacao_sigla"] + "-" + processar["sist_varredura_sigla_tipo"] + "." + processar["varredura"] + " inserida no BD.")
        else:
            print("Erro ao enviar os dados para gravação no BD:", response.status_code)
            logger.error (f"Erro ao salvar os dados no BD: {response.text}")
  except paramiko.SSHException as e:
    print(f"Erro ao executar o comando remoto: {e}")
    logger.error (f"Erro ao executar o comando remoto: {e}")
         
def processaJuris (cnnssh,processar):
  try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())    
    ssh.connect(hostname=processar["sist_varredura_ip_acesso"], username=processar["sist_varredura_usuario"], password=processar["sist_varredura_senha"])
    
    #comando = "docker exec mn.sonar_cli bash -c '" + processar["sist_varredura_comando"] + "'" 
    comando = processar["sist_varredura_comando"] 
    print(comando)
    response = requests.get (f"{url_base_aplicacoes}{processar['sistema_varredura']}")
    app_usuario_servico=""  
    if response.status_code == 200:
        app_usuario_servico = response.json().get('usuario_servico')
    cmd = comando.replace( "{aplicacao}", processar["aplicacao_sigla"].lower())
    cmd = cmd.replace( "{app_host}", processar["sist_varredura_host"])
    cmd = cmd.replace( "{app_token}", processar["sist_varredura_token"])
    cmd = cmd.replace( "{user}", app_usuario_servico) #processar["sist_varredura_usuario"])  
    cmd = cmd.replace( "{password}", os.getenv('SENHA_SERVICO'))  #processar["sist_varredura_senha"])  "@dm1n"
    print (f"2º passo: Comando: {cmd}")
    #cmd = "docker exec mn.sonar_cli bash -c 'sonar-scanner -X -Dsonar.projectKey=jurisprudencia -Dsonar.sources=app/jurisprudencia "
    #cmd = cmd + "-Dsonar.host.url=http://192.168.0.12:32768 -Dsonar.login=servico -Dsonar.password=@dm1n -Dsonar.exclusions=**/*.java'"
    cmd = f"sonar-scanner -X -Dsonar.projectKey=" + processar["aplicacao_sigla"].lower() + " -Dsonar.sources=app/" + processar["aplicacao_sigla"].lower() 
    cmd = cmd + f" -Dsonar.host.url=" + processar["url_codigo_fonte"] + " -Dsonar.login=servico -Dsonar.password=@dm1n -Dsonar.exclusions=**/*.java"
    print("---")
    print (cmd) 
    try:
        stdin,stdout,stderr = ssh.exec_command(cmd)
        stdin.write("docker\n")
        stdin.flush()    
        stdin.close()
        if stderr.channel.recv_exit_status() == 0:
            print("Análise realizada com sucesso!")
            logger.info (f"Análise da aplicação " + processar["aplicacao_sigla"] + "realizada com sucesso.")
        else:
            logger.error (f"Erro ao executar a varredura: {stderr.readlines()}")
    except paramiko.SSHException as e:
        print(f"Erro ao executar o comando remoto: {e}")
        logger.error (f"Erro ao executar o comando remoto: {e}")
    # finalizar processamento
    ssh.close()
    # retornar o resultado
    resultado = {
      "aplicacao": processar["aplicacao_id"],
      "varredura": processar["varredura"],
      "sistemas_varredura": processar["sistema_varredura"],
      "resultado": jsondoc,
    }   
    return (resultado)
  
    
  except paramiko.SSHException as e:    
    print(f"Erro ao conectar ao servidor remoto: {e}")
    logger.error (f"Erro ao conectar ao servidor remoto: {e}")             
                 
def processaGarimpo (processar):
  try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())    
    ssh.connect(hostname=processar["sist_varredura_ip_acesso"], username=processar["sist_varredura_usuario"], password=processar["sist_varredura_senha"])
    
    #comando = "docker exec mn.sonar_cli bash -c '" + processar["sist_varredura_comando"] + "'" 
    comando = processar["sist_varredura_comando"] 
    print(comando)
    response = requests.get (f"{url_base_aplicacoes}{processar['sistema_varredura']}")
    app_usuario_servico=""  
    if response.status_code == 200:
        app_usuario_servico = response.json().get('usuario_servico')
    cmd = comando.replace( "{aplicacao}", processar["aplicacao_sigla"].lower())
    cmd = cmd.replace( "{app_host}", processar["sist_varredura_host"])
    cmd = cmd.replace( "{app_token}", processar["sist_varredura_token"])
    cmd = cmd.replace( "{user}", app_usuario_servico) #processar["sist_varredura_usuario"])  
    cmd = cmd.replace( "{password}", "@dm1n")  #processar["sist_varredura_senha"])  
    print (f"2º passo: Comando: {cmd}")
    #cmd = "docker exec mn.sonar_cli bash -c 'sonar-scanner -X -Dsonar.projectKey=deposito-web -Dsonar.sources=app/deposito-web "
    #cmd = cmd + "-Dsonar.host.url=http://192.168.0.12:32768 -Dsonar.token=squ_a3331308f1483f4f988f220c376d34853f0a2eb4 "
    #cmd = cmd + "-Dsonar.login=servico -Dsonar.password=@dm1n -Dsonar.exclusions=**/*.java'"
    cmd = "sonar-scanner -X -Dsonar.projectKey=" + processar["aplicacao_sigla"].lower() + " -Dsonar.sources=app/" + processar["aplicacao_sigla"].lower()
    cmd = cmd + " -Dsonar.host.url=" + processar["url_codigo_fonte"] + " -Dsonar.token=" + processar["sist_varredura_token"] 
    cmd = cmd + " -Dsonar.login=servico -Dsonar.password=@dm1n -Dsonar.exclusions=**/*.java'"
        
    print("---")
    print (cmd) 
    try:
        stdin,stdout,stderr = ssh.exec_command(cmd)
        stdin.write("docker\n")
        stdin.flush()    
        stdin.close()
        if stderr.channel.recv_exit_status() == 0:
            print("Análise realizada com sucesso!")
            logger.info (f"Análise da aplicação " + processar["aplicacao_sigla"] + "realizada com sucesso.")
        else:
            logger.error (f"Erro ao executar a varredura: {stderr.readlines()}")
    except paramiko.SSHException as e:
        print(f"Erro ao executar o comando remoto: {e}")
        logger.error (f"Erro ao executar o comando remoto: {e}")
    # finalizar processamento
    ssh.close()
    # retornar o resultado
    resultado = {
      "aplicacao": processar["aplicacao_id"],
      "varredura": processar["varredura"],
      "sistemas_varredura": processar["sistema_varredura"],
      "resultado": jsondoc,
    }   
    return (resultado)
  
    
  except paramiko.SSHException as e:    
    print(f"Erro ao conectar ao servidor remoto: {e}")
    logger.error (f"Erro ao conectar ao servidor remoto: {e}")
              
def get_sistema_varredura(resultado):
  retorno=''
  if "Sonar way" in resultado['qualityGate']['name']:
    retorno = "SonarQube"
  elif "Checkmarx" in resultado['qualityGate']['name']:
    retorno = "Checkmarx"
  elif "Owasp dependency-check" in resultado['qualityGate']['name']:
    retorno = "Owasp dependency-check"
  else:
    retorno = "Outro"
  return (retorno)

def processa_resultado(novo_resultado):
  try:
    data_execucao = novo_resultado['analysedAt']
    aplicacao = novo_resultado['project']['key'] 
    #print(aplicacao)
    #print(data_execucao)
    apps = requests.get(url_base_aplicacoes) #, headers=headears)
    if apps.status_code == 200:
      for app in apps.json().get("results"):
        if app['sigla'] == aplicacao.upper():
          aplicacao_id = app['id']
          print(aplicacao_id)
          versoes = requests.get(f"{url_base_aplicacoes}{aplicacao_id}/versoes")  #, headers=headears)
          if versoes.status_code == 200:
            #print(versoes.json())
            for versao in versoes.json().get("results"):
              if versao['nome_versao'] == novo_resultado['branch']['name']:
                versao_id = versao['id']
                break
          else:
            return(versoes.status_code)
          break
    else:
      return(apps.status_code)  
    # obtem o sistema de varredura que gerou o resultado
    sistemas_varredura = get_sistema_varredura(novo_resultado)
    # monta o resultado para ser armazenamento
    string_resultado={
      "aplicacao": versao_id,
      "resultado": novo_resultado,
      "data_resultado": data_execucao,
      "sistema_varredura": sistemas_varredura
      }

    #json_data = json.dumps(string_resultado)
    #return (json_data)
    return (string_resultado)
  except Exception as e:
    return (f"Erro ao processar o resultado: {e}")
  
#resultado = requests.post(url_base_resultado, headers=headears, data=novo_resultado)  
#print(resultado.status_code)
#assert resultado.status_code == 201
#
#aplicacao: Aplicação à qual o resultado pertence.
#resultado: Resultado da varredura de segurança.
#data_resultado: Data do resultado da varredura.
#sistema_varredura: Sistema de varredura que gerou o resultado.
