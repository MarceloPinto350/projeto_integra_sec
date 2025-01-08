import requests, time, logging, json, paramiko, subprocess, os 

from django.utils import timezone

from seguranca.serializers import ResultadoScanSerializer
#from seguranca.utils import varredura_result
from ..models import VersaoAplicacao

from rest_framework.response import Response

from celery import shared_task

#headears = {'Authorization':'Token 61a384f801cb080e0c8f975c7731443b51c9f02e'}
headers = {'Content-Type': 'application/json'}
url_api = os.getenv('URL_API')
url_base_aplicacoes = f'{url_api}/v2/aplicacoes/'

logger = logging.getLogger(__name__)  

report_path = '/src/report'
report_name = 'dependency-check-report.json'

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
  try:
    # baixar o código fonte da aplicação
    #ssh.connect(hostname='192.168.0.10', username='docker', password='docker")
    ssh.connect(hostname=processar["sist_varredura_ip_acesso"], username=processar["sist_varredura_usuario"], password=processar["sist_varredura_senha"])
    # 1º passo: clonar na máquina do OWASP-CDC a imagem da aplicação a ser varrida
    #comando = f"docker exec mn.owasp_dc bash -c 'cd /src && rm -rf DVWA && rm -f dc-report.json && git clone {dvwa_fonte}'\n"
    #comando = f"docker exec mn.owasp_dc bash -c 'cd /src && rm -rf {processar['aplicacao_sigla'].lower()} && rm -f {report_path}/{processar['aplicacao_sigla'].lower()}/"
    comando = f"rm -rf src/{processar['aplicacao_sigla'].lower()} && rm -rf {report_path}/{processar['aplicacao_sigla'].lower()} && cd src && git clone {processar['url_codigo_fonte']}"
    comando = f"{comando} && mv -f {processar['aplicacao_sigla']} {processar['aplicacao_sigla'].lower()}" 
    print (f"1º passo: Comando: {comando}")   
    try:  
      stdin,stdout,stderr = ssh.exec_command(comando)
      #stdin.write("docker\n")
      #stdin.flush()    
      #stdin.close()
      cod_erro = stderr.channel.recv_exit_status()
      erro = stderr.readlines()
      saida = stdout.readlines()
      if cod_erro == 0:
        print(f"Clonagem da aplicação {processar['aplicacao_sigla']} realizada com sucesso!")
        logger.info (f"Clonagem da aplicação {processar['aplicacao_sigla']} realizada com sucesso!")
        #2º passo: executar a varredura da aplicação
        #comando = "docker exec mn.owasp_dc bash -c '/bin/dependency-check.sh --project DVWA --scan /src/DVWA --format JSON --out /src/report-dvwa -n'"
        #/bin/dependency-check.sh --project {aplicacao} --scan /src/{aplicacao} --format JSON --out /src/report/{aplicacao} -n
        #comando = f"{comando} --nvdApiKey cd0c05ca-2b15-4034-9ae6-490fb505f439'"
        #comando = "docker exec mn.owasp_dc bash -c '" + processar["sist_varredura_comando"] + "'" 
        comando = processar["sist_varredura_comando"]
        comando = comando.replace("{aplicacao}", processar["aplicacao_sigla"].lower())
        comando = comando.replace("{report_path}", report_path)
        print (f"2º passo: Comando: {comando}")
        try:
          stdin,stdout,stderr = ssh.exec_command(comando)
          cod_erro = stderr.channel.recv_exit_status()
          erro = stderr.readlines()
          saida = stdout.readlines()
          if cod_erro == 0:
            print(f"Análise da aplicação {processar['aplicacao_sigla']} realizada com sucesso!")
            logger.info (f"Análise da aplicação {processar['aplicacao_sigla']} realizada com sucesso!")
            #3º passo: carregar o resultado da varredura
            #comando = "docker exec mn.owasp_dc cat /src/report/<aplicacao>/dependency-check-report.json"
            #comando = f"docker exec mn.owasp_dc cat {report_path}/{processar['aplicacao_sigla'].lower()}/{report_name}"
            comando = f"cat {report_path}/{processar['aplicacao_sigla'].lower()}/{report_name}"
            print(f"3º passo: Comando: {comando}")
            try:
              #baixar o arquivo de resultado da varredura para a máquina remota do docker
              #cmd = f"docker cp mn.owasp_dc:{report_path}/{processar['aplicacao_sigla'].lower()}/{report_name} {processar['aplicacao_sigla'].lower()}-{report_name}"
              stdin,stdout,stderr = ssh.exec_command(comando) 
              cod_erro = stderr.channel.recv_exit_status()
              erro = stderr.readlines()
              saida = stdout.readlines()
              # copiar o arquivo localmente para a pasta midia
              #ssh.connect(hostname=processar["sist_varredura_ip_acesso"], username=processar["sist_varredura_usuario"], password=processar["sist_varredura_senha"])
              # testar se retornou erro
              if cod_erro == 0:
                print("Arquivo obtido com sucesso!")
                #dados = json.loads(saida.replace("\\','").replace("[\"','").replace("\"]','"))
                string = str(saida)
                #print (dados)
                string = string.replace("'","")
                string = string.replace("\\","")
                # converter o texto em json
                json_doc = ""
                dados = json.loads(string) 
                for item in dados:
                  json_doc = item
                #payload = json.dumps(dados,indent=3)
                #headers = {'Content-Type': 'application/json'}
                versao = VersaoAplicacao.objects.filter(aplicacao=processar["aplicacao_id"]).order_by('-data_lancamento').first()
                #print(f"Ferramenta: {ferramenta} - Versão: {versao.nome_versao} ==> {versao.id}")
                versao_id = versao.id
                # busca a último varredura realizada ainda em aberto
                string_resultado={
                  "data_resultado": timezone.now(),
                  "resultado": json.dumps(json_doc,indent=3),
                  "aplicacao": versao_id,       #processar["aplicacao_id"],
                  "varredura": processar["varredura"],
                  "sistema_varredura": processar["sistema_varredura"]
                }
                print(string_resultado)
                # gravando o resultado na base de dados
                ssh.close()
                serializer =  ResultadoScanSerializer(data=string_resultado)
                if serializer.is_valid():
                  serializer.save()
                  print(f"Resultado salvo com sucesso: {serializer.data}")
                  logger.info (f"Resultado salvo com sucesso: {serializer.data}")
                  return requests.Response(serializer.data, status=201)
                else:
                  print(f"Erro ao salvar o resultado: {serializer.errors}")
                  logger.erro (f"Erro ao salvar o resultado: {serializer.errors}")
                  return requests.Response(serializer.errors, status=400)
                # response = requests.post(f'{url_api}/v1/resultados/',data=payload, headers=headers)
                # if response.status_code == 201:
                #     print("Dados inseridos no BD!")
                #     logger.info (f"Resultado da análise "+ processar["aplicacao_sigla"] + "-" + processar["sist_varredura_sigla_tipo"] + "." + processar["varredura"] + " inserida no BD.")
                # else:
                #     print("Erro ao enviar os dados para gravação no BD:", response.status_code)
                #     logger.error (f"Erro ao salvar os dados no BD: {response.text}")
                #     jsondoc["erros"] = 1
              else:
                print (f"Erro ao copiar o arquivo de resultado.\n {erro}")
                logger.error (f"Erro ao copiar o arquivo de resultado:\n {erro}")
                jsondoc["erros"] = 1  
            except paramiko.SSHException as e:
              print(f"Erro ao executar o comando remoto: {e}")
              logger.error (f"Erro ao executar o comando remoto: {e}")
              jsondoc["erros"] = 1
          else:
            print (f"Erro ao executar a varredura.\n {erro}")
            logger.error (f"Erro ao executar a varredura:\n {erro}")
            jsondoc["erros"] = 1    
        except paramiko.SSHException as e:
          print(f"Erro ao executar o comando remoto: {e}")
          logger.error (f"Erro ao executar o comando remoto: {e}")
          jsondoc["erros"] = 1
      else:
        print (f"Erro ao clonar o repositório da aplicação.\n {erro}")
        logger.error (f"Erro ao clonar o repositório da aplicação:\n {erro}")
        jsondoc["erros"] = 1
    except paramiko.SSHException as e:
        print(f"Erro ao executar o comando remoto: {e}")
        logger.error (f"Erro ao executar o comando remoto: {e}")  
        jsondoc["erros"] = 1
  except paramiko.SSHException as e:
    print(f"Erro ao executar o comando remoto: {e}")
    logger.error (f"Erro ao executar o comando remoto: {e}")
    jsondoc["erros"] = 1
  finally:
    # finalizar processamento
    ssh.close()
    # retornar o resultado
    resultado = {
      "aplicacao": processar["aplicacao_id"],
      "varredura": processar["varredura"],
      "sistemas_varredura": processar["sistema_varredura"],
      "resultado": jsondoc,
    }   
    print()
    print (f"Resultado da varredura: {resultado}")  
    return (resultado)
      
      
      # ## copia para máquina local
      # arq_origem = f"{report_path}/{processar['aplicacao_sigla'].lower()}/{report_name}"
      # nome_destino = {processar['aplicacao_sigla'].lower()}-{report_name}
      # arq_destino = f"midia/{nome_destino}"
      # cmd = f"scp {processar['sist_varredura_usuario']}@{processar['sist_varredura_ip_acesso']}:{arq_origem} {arq_destino}" 
      # # copia o arquivo para pasta local
      # try:
      #   subprocess.run(cmd, shell=True,check=True)
      #   # processar arquivo de resultado
      #   with open(arq_destino, 'r') as arquivo:
      #     dados = json.load(arquivo)
      #   # trocando caracteres inválidos
      #   for chave, valor in dados.items():
      #       if isinstance(valor, str):
      #           dados[chave] = valor.replace('\\', '').replace('["', '').replace('"]', '')
      #   #salvando o arquivo de resultado
      #   arq_destino = f"midia/novo_{nome_destino}"
      #   try:
      #     with open(arq_destino, 'w') as arquivo:
      #       dados = json.dump(dados, arquivo,indent=3)
      #       #print("Arquivo de resultado carregado com sucesso!")  
      #       #payload = json.dumps(dados,indent=3)
      #     with open(arq_destino, 'r') as arquivo:
      #       dados = json.load(arquivo)
      #     #print (f"Resultado da varredura: {dados}")
      #     string_resultado={
      #         "data_resultado": timezone.now(),
      #         "resultado": json.dumps(dados,indent=3),
      #         "aplicacao": processar["aplicacao_id"],
      #         "varredura": processar["varredura"],      
      #         "sistema_varredura": processar["sistema_varredura"]
      #         }
      #     time.sleep(1) # aguarda o carregamento do arquivo
      #     #print("Passou aqui...",string_resultado)
      #     # gravando o resultado na base de dados
      #     #resultado = varredura_result.processa_resultado(request.data)
      #     # validar o serializer e salvar dados no BD
      #     try:  
      #       serializer =  ResultadoScanSerializer(data=string_resultado)
      #       time.sleep(2) # aguarda o carregamento do arquivo
      #       if serializer.is_valid():
      #         serializer.save()
      #         #print(f"Resultado salvo com sucesso: {serializer.data}")
      #         logger.info (f"Resultado salvo com sucesso: {serializer.data}")
      #         #return Response(serializer.data, status=201)
      #       else:
      #         print(f"Erro ao salvar o resultado: {serializer.errors}")
      #         #print(f"Serializer: {string_resultado}")
      #         logger.error (f"Erro ao salvar o resultado: {serializer.errors}")
      #         return Response({"varredura": None, "erro": processar["varredura"]}, status=400)
      #       #response = requests.post('http://192.168.0.22:8000/api/v1/resultados/',data=dados, headers=headers)
      #     except Exception as e:
      #       print(f"Erro ao gravar o resultado: {e}")
      #       logger.error (f"Erro ao gravar o resultado: {e}")
      #   except Exception as e:
      #     print(f"Erro ao salvar o arquivo de resultado: {e}")
      #     logger.error (f"Erro ao salvar o arquivo de resultado: {e}")
      # except subprocess.CalledProcessError as e:
      #   print(f"Erro ao copiar o arquivo de resultado: {e}")
      #   logger.error (f"Erro ao copiar o arquivo de resultado: {e}")  
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
    # print()
    # print (f"Resultado da varredura: {resultado}")  
    # return (resultado)
  
  # except paramiko.SSHException as e:    
  #   print(f"Erro ao conectar ao servidor remoto: {e}")
  #   logger.error (f"Erro ao conectar ao servidor remoto: {e}")

         
