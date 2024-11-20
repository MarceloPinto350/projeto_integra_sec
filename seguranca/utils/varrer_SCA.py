import time, logging, json, paramiko, subprocess

from django.utils import timezone

from seguranca.serializers import ResultadoScanSerializer
#from seguranca.utils import varredura_result
from rest_framework.response import Response

from celery import shared_task

#headears = {'Authorization':'Token 61a384f801cb080e0c8f975c7731443b51c9f02e'}
headers = {'Content-Type': 'application/json'}
url_base = "http://192.168.0.22:8000/api/v2"
url_base_aplicacoes = f"{url_base}/aplicacoes/"

logger = logging.getLogger(__name__)  

report_path = '/src/report'
report_name = 'dependency-check-report.json'

jsondoc = {
      "erros": 0, 
      "falhas": 0, 
      "testes": 0, 
      "tempo": 0
    }
    
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
  print()
  try:
    # define a conexão SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # baixar o código fonte da aplicação
    #ssh.connect(hostname='192.168.0.10', username='docker', password='docker")
    ssh.connect(hostname=processar["sist_varredura_ip_acesso"], username=processar["sist_varredura_usuario"], password=processar["sist_varredura_senha"])
    # 1º passo: clonar na máquina do OWASP-CDC a imagem da aplicação a ser varrida
    #comando = f"docker exec mn.owasp_dc bash -c 'cd /src && rm -rf DVWA && rm -f dc-report.json && git clone {dvwa_fonte}'\n"
    comando = f"docker exec mn.owasp_dc bash -c 'cd /src && rm -rf {processar['aplicacao_sigla'].lower()} && rm -f {report_path}/{processar['aplicacao_sigla'].lower()}/"
    comando = comando + f"{report_name} && git clone {processar['url_codigo_fonte']} '\n" 
    print (f"1º passo: Comando: {comando}")   
    
    ### comentado para testar a varredura com dados locais - desabilitar para homologação     
    # try:  
    #     stdin,stdout,stderr = ssh.exec_command(comando)
    #     stdin.write("docker\n")
    #     stdin.flush()    
    #     stdin.close()
    #     # testar se retornou erro
    #     if stderr.channel.recv_exit_status() == 0:
    #     #if stderr.readlines() != "[]":
    #         print("Clonagem realizada com sucesso!")
    #         logger.info (f"Clonagem da aplicação " + processar["aplicacao_sigla"] + "realizada com sucesso.")
    #     else:
    #         #print ("Erro ao clonar o repositório da aplicação.")
    #         logger.error (f"Erro ao clonar o repositório da aplicação: {stderr.readlines()}")
    # except paramiko.SSHException as e:
    #     print(f"Erro ao executar o comando remoto: {e}")
    #     logger.error (f"Erro ao executar o comando remoto: {e}")  
        
    # 2º passo: executar a varredura da aplicação
    #comando = "docker exec mn.owasp_dc bash -c '/bin/dependency-check.sh --project DVWA --scan /src/DVWA --format JSON --out /src/report-dvwa -n'"
    comando = "docker exec mn.owasp_dc bash -c '" + processar["sist_varredura_comando"] + "'" 
    #comando = f"{comando} --nvdApiKey cd0c05ca-2b15-4034-9ae6-490fb505f439'"
    #comando = processar.sist_varredura_comando 
    cmd = comando.replace( "{aplicacao}", processar["aplicacao_sigla"].lower())
    print (f"2º passo: Comando: {cmd}")
    try:
        stdin,stdout,stderr = ssh.exec_command(cmd)
        stdin.write("docker\n")
        stdin.flush()    
        stdin.close()
        #if stderr.channel.recv_exit_status() == 0:
        if stderr.readlines() == []:
            #print("Análise realizada com sucesso!")
            logger.info (f"Análise da aplicação " + processar["aplicacao_sigla"] + "realizada com sucesso.")
        else:
            print (f"Erro ao executar a varredura. stderr: {stderr.readlines()}; stdout: {stdout.readlines()}")
            logger.error (f"Erro ao executar a varredura: stderr: {stderr.readlines()}; stdout: {stdout.readlines()}")
    except paramiko.SSHException as e:
        print(f"Erro ao executar o comando remoto: {e}")
        logger.error (f"Erro ao executar o comando remoto: {e}")
    
    #3º passo: carregar o resultado da varredura
    #comando = "docker exec mn.owasp_dc cat /src/report/<aplicacao>/dependency-check-report.json"
    comando = f"docker exec mn.owasp_dc cat {report_path}/{processar['aplicacao_sigla'].lower()}/{report_name}"
    print()
    print(f"3º passo: Comando: {comando}")
    try:
      #baixar o arquivo de resultado da varredura para a máquina remota do docker
      cmd = f"docker cp mn.owasp_dc:{report_path}/{processar['aplicacao_sigla'].lower()}/{report_name} {processar['aplicacao_sigla'].lower()}-{report_name}"
      stdin,stdout,stderr = ssh.exec_command(cmd) 
      stdin.write("docker\n")
      stdin.flush()
      stdin.close()
      # copiar o arquivo localmente para a pasta midia
      arq_origem = f"{processar['aplicacao_sigla'].lower()}-{report_name}"
      arq_destino = f"midia/{arq_origem}"
      cmd = f"scp {processar['sist_varredura_usuario']}@{processar['sist_varredura_ip_acesso']}:{arq_origem} {arq_destino}" 
      # copia o arquivo para pasta local
      try:
        subprocess.run(cmd, shell=True,check=True)
        # processar arquivo de resultado
        with open(arq_destino, 'r') as arquivo:
          dados = json.load(arquivo)
        # trocando caracteres inválidos
        for chave, valor in dados.items():
            if isinstance(valor, str):
                dados[chave] = valor.replace('\\', '').replace('["', '').replace('"]', '')
        #salvando o arquivo de resultado
        arq_destino = f"midia/novo_{arq_origem}"
        try:
          with open(arq_destino, 'w') as arquivo:
            dados = json.dump(dados, arquivo,indent=3)
            #print("Arquivo de resultado carregado com sucesso!")  
            #payload = json.dumps(dados,indent=3)
          with open(arq_destino, 'r') as arquivo:
            dados = json.load(arquivo)
          #print (f"Resultado da varredura: {dados}")
          string_resultado={
              "data_resultado": timezone.now(),
              "resultado": json.dumps(dados,indent=3),
              "aplicacao": processar["aplicacao_id"],
              "varredura": processar["varredura"],      
              "sistema_varredura": processar["sistema_varredura"]
              }
          time.sleep(1) # aguarda o carregamento do arquivo
          #print("Passou aqui...",string_resultado)
          # gravando o resultado na base de dados
          #resultado = varredura_result.processa_resultado(request.data)
          # validar o serializer e salvar dados no BD
          try:  
            serializer =  ResultadoScanSerializer(data=string_resultado)
            time.sleep(2) # aguarda o carregamento do arquivo
            if serializer.is_valid():
              serializer.save()
              #print(f"Resultado salvo com sucesso: {serializer.data}")
              logger.info (f"Resultado salvo com sucesso: {serializer.data}")
              #return Response(serializer.data, status=201)
            else:
              print(f"Erro ao salvar o resultado: {serializer.errors}")
              #print(f"Serializer: {string_resultado}")
              logger.error (f"Erro ao salvar o resultado: {serializer.errors}")
              return Response({"varredura": None, "erro": processar["varredura"]}, status=400)
            #response = requests.post('http://192.168.0.22:8000/api/v1/resultados/',data=dados, headers=headers)
          except Exception as e:
            print(f"Erro ao gravar o resultado: {e}")
            logger.error (f"Erro ao gravar o resultado: {e}")
        except Exception as e:
          print(f"Erro ao salvar o arquivo de resultado: {e}")
          logger.error (f"Erro ao salvar o arquivo de resultado: {e}")
      except subprocess.CalledProcessError as e:
        print(f"Erro ao copiar o arquivo de resultado: {e}")
        logger.error (f"Erro ao copiar o arquivo de resultado: {e}")  
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
    print()
    print (f"Resultado da varredura: {resultado}")  
    return (resultado)
  
  except paramiko.SSHException as e:    
    print(f"Erro ao conectar ao servidor remoto: {e}")
    logger.error (f"Erro ao conectar ao servidor remoto: {e}")

         
