import logging, paramiko, paramiko.ssh_exception,json     

# configurar o log
logger = logging.getLogger(__name__)
                    
def conecta_ssh(cliente, host, usuario, senha):    
    """
    conecta_ssh - Função para conectar via SSH em um host remoto

    Args:
        cliente: Cliente SSH já configurado
        host (url): host remoto
        usuario (string): usuário para autenticação
        senha (string): senha para autenticação

    Returns:
        boolean: conectado (True) ou não conectado (False)
    """
    # parâmetros de conexão SSH
    #cliente = paramiko.SSHClient()
    #cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #cliente.load_system_host_keys()

    try:
        cliente.connect(hostname=host, username=usuario, password=senha)
        return (True)
    except paramiko.ssh_exception.AuthenticationException as e:
        print(f'Erro ao autenticar no host {host} via SSH: {e}')
        logger.error(f'Erro ao autenticar no host {host} via SSH: {e}')  
        return (False)
    except paramiko.ssh_exception.NoValidConnectionsError as e1:
        print(f'Erro ao conectar no host {host} via SSH: {e1}')
        logger.error(f'Erro ao conectar no host {host} via SSH: {e1}')  
        return (False)
    except paramiko.ssh_exception.SSHException as e2:
        print(f'Erro ao acessar o host {host} via SSH: {e2}')  
        logger.error(f'Erro ao acessar o host {host} via SSH: {e2}')  
        return (False)

def exec_comando_ssh(cliente, comando):
    """
    exec_comando_ssh - Função para executar um comando remoto via SSH

    Args:
        comando (string): comando a ser executado

    Returns:
        dictionary: retorno do comando (stdout, stderr, erro)
    """
    print(f'Dados do cliente: {cliente}.\n')
    print(f'Executando o comando remoto {comando}...\n')
    logger.info(f'Executando o comando remoto {comando}...')
    try:
        stdin,stdout,stderr = cliente.exec_command(comando)
        stdin.write('docker\n')
        stdin.flush()    
        stdin.close()
        erro = stderr.read().decode('utf-8')
        saida = stdout.read().decode('utf-8')
        retorno = {
            "stdout": saida,
            "stderr": erro,
            "erro": stderr.channel.recv_exit_status()
        }
    except paramiko.SSHException as e:
        print(f'Erro ao executar o comando remoto {comando}: {e}')
        logger.error(f'Erro ao executar o comando remoto {comando}: {e}')
        retorno = {
            "stdout": None,
            "stderr": None,
            "erro": e
        }
    finally:
        return retorno

def retorna_stout_ssh(cliente, comando, tipo):  
    """
    retorna_stout_ssh - Função para executar um comando remoto via SSH e retornar o resultado no formato especificado
    
    Args:
        comando (string): comando a ser executado
        tipo (string): tipo de retorno (JSON, XML, TXT

    Returns:
        string: contendo o resultado do comando no formato especificado
    
    """  
    try:
        stdin,stdout,stderr = cliente.exec_command(comando)
        stdin.write('docker\n')
        stdin.flush()    
        stdin.close()
        resultado = stdout.readlines()
        # for linha in resultado:
        #     print (linha);
        #print(resultado[0])
        
        if tipo=='JSON':
            retorno = json.loads(resultado[0])
        #elif tipo=='XML':
        #    retorno = stdout.readlines()
        else:
            retorno = resultado
    except paramiko.SSHException as e:
        #print(f'Erro ao executar o comando remoto {comando}: {e}')
        logger.error(f'Erro ao executar o comando remoto {comando}: {e}')
        retorno = None
    return retorno
    
# def get_ultima_versao_app(aplicacao_id):
#     versao = 3
#     return versao
   
# def get_sistemas_varredura(aplicacao_id):
#     sistemas_varredura =  [
#         {
#             "id": 1,
#             "nome": "SonarQube",
#             "tipo": "SAST",
#             "status": "Ativo",
#             "url": "mn.sonar_cli"},
#         {   "id": 2,
#             "nome": "Owasp Dependency Check",
#             "tipo": "SCA",
#             "status": "Ativo",
#             "url": "mn.owasp_dc"},
#     ]
#     return json.dumps(sistemas_varredura)


# def testa():
#     # 1) coletar os dados da aplicação (última versão e sistemas de varredura)
#     # 2) coletar as informações sobre o serviço SSH (docker) para se conectar a ele 
#     # 2.1) conectar ao serviço SSH (docker)
#     # 3) fazer loop para cada sistema de varredura
#     # 3.1) executar a varredura da aplicação (SonarQube, Owasp dependency-check)
#     # 3.2) se não usar webhook, coletar os resultados da varredura
#     # 3.3) armazenar os resultados da varredura
#     # 4) fechar a conexao SSH
#     # 5) encerrar a rotina
      
#     appseg_base = 'http://localhost:8000/api/v2/'
#     #http://192.168.0.22:8000/api/v2/aplicacoes/1/ 
#     headears = {'Authorization':'Token 61a384f801cb080e0c8f975c7731443b51c9f02e'}
#     app_id='1'
    
#     print('---')
#     print (get_ultima_versao_app(app_id))
#     print ("---")
#     print (get_sistemas_varredura(app_id))
    
    
#     aplicacao = requests.get(f'{appseg_base}aplicacoes/{app_id}', headers=headears)
#     if aplicacao.status_code == 200:
#         app = {
#             "id":aplicacao.json().get('id'),
#             "Sigla": {aplicacao.json().get('sigla')},
#             "url_fonte": {aplicacao.json().get('url_fonte')},
#             "versoes": {aplicacao.json().get('versoes')},
#             "sistemas_varredura": {aplicacao.json().get('sistemas_varredura')}
#             "versao_atual": {aplicacao.json().get('versoes').last()}
#         }
#         print (json.loads(app))
#         #print (f"Aplicacao: {aplicacao.json().get('nome')}, Sigla: {aplicacao.json().get('sigla')}") #, Última Versão: {aplicacao.json().get('versoes').last}")
#         #print (f"Última Versão: {get_ultima_versao_app(app_id)}")
#         # obtem os sistemas de varredura habilitados para a aplicação
#         #sistemas_varredura = aplicacao.json().get('sistemas_varredura')
#         #print (sistemas_varredura)
#     else:
#         print (f"Erro: {aplicacao.status_code}")
#     print('===--- ### ---===')
#     aplicacao = requests.get(f'{appseg_base}aplicacoes/{app_id}', headers=headears)
#     #aplicacao = Aplicacao.objects.get(pk=app_id)
#     versoes = requests.get(f'{appseg_base}versoes', headers=headears)
#     print(versoes.json())
    
    
#     # url_base_aplicacoes = 'http://localhost:8000/api/v2/aplicacoes/'
#     # url_base_versoes = 'http://localhost:8000/api/v2/versoes/'
#     # docker_host = '192.168.0.3'
#     # sonar_host = 'http://192.168.0.9:32768'
#     # sonar_api = f'{sonar_host}/api'
#     # docker_server = 'http://192.168.0.9:2375'
#     # dvwa_fonte = 'https://github.com/MarceloPinto350/DVWA.git'
#     # sonar_dvwa_token = 'squ_0b2cafe9d40615f6ec9dbb3ba037085fd7019363'   # mmpinto
    
#     # exemplo de get usando o token de acesso e a API
#     # GET Aplicações
#     #
#     # aplicacoes = requests.get(url_base_aplicacoes, headers=headears)
#     # print (aplicacoes.json())
#     # # testar se o status da requisição foi bem sucedido
#     # assert aplicacoes.status_code == 200
#     # # Testar a qantidade de resultados
#     # assert aplicacoes.json()['count'] == 2
#     #
    

# print('--- ----')
# testa()

# ssh_connect.close()

#     if conecta_ssh('192.168.0.13', 'docker', 'docker'):
#         # testar comandos SSH...
#         comando = "docker exec mn.owasp_dc bash -c '/bin/dependency-check.sh --scan /src/DVWA --format ALL --out /src/report -n'"
        
#         # validar o resultado
        
#         resultado = exec_comando_ssh("docker inspect owasp_dc")  
#         #for val in resultado["stdout"]:
#         #    print(val)
        
#         # localizar o valor do campo "Mountpoint" no resultado da inspeção do container (docker inspect owasp_dc)
#         print(resultado["stdout"][5])
#         # filtrar o valor do campo "Mountpoint" no resultado da inspeção do container (docker inspect owasp_dc)
#         caminho = ((resultado["stdout"][5].split(':')[1].strip().replace('"','')).replace(',',''))+'/src/report'
#         #print((resultado["stdout"][5].split(':')[1].strip().replace('"','')).replace(',',''))
#         print(caminho)  
        
#         resultado = exec_comando_ssh("docker exec mn.owasp_dc bash -c 'cat /src/report/dependency-check-report.json'")
#         print(resultado.keys())     
#         #print(resultado["stdout"][0])
#         print("*-*-*-*-*")
#         resultado = retorna_stout_ssh("docker exec mn.owasp_dc bash -c 'cat /src/report/dependency-check-report.json'", 'JSON')
        
#         print (resultado.keys())
#         print (json.loads(resultado))
#         #for valor in resultado.items[0].itens():
#         #    print(valor[0])
        
#     else: 
#         print('Não foi possível conectar no docker via SSH')    

# host='192.168.0.13'
# comando = 'hostname'

#print(f'Testando conexão SSH com o host {host}... {conecta_ssh(host,"docker","docker")}')
#print(f"Testando execução de comando SSH no host {host}... {exec_comando_ssh('docker exec mn.owasp_dc uname -s')}")

#print('---')
#host='192.168.0.19'

#print(f'Testando conexão SSH com o host {host}... {conecta_ssh(host,"docker","docker")}')
#print(f'Testando execução de comando SSH no host {host}... {exec_comando_ssh(comando)}')      

# 1º passo: clonar na máquina do Sonar_CLI a imagem da aplicação a ser varrida
# comando = f"docker exec mn.sonar_cli bash -c 'cd app && rm -rf DVWA && git clone {dvwa_fonte}'\n"
# print ("Preparando para varredura...")
# print (f"Comando: {comando}")        
# try:  
#     stdin,stdout,stderr = ssh.exec_command(comando)
#     stdin.write('docker\n')
#     stdin.flush()    
#     stdin.close()
#     print(stdout.readlines())
#     print(stderr.readlines())    
#     if "Cloning into 'DVWA'" in stderr.readlines():
#         print("Repositório clonado com sucesso!")
#     else:
#         print("Erro ao clonar o repositório!")
# except paramiko.SSHException as e:
#     print(f'Erro ao executar o comando remoto: {e}')
# print()

# 2ª passo: criado webservice para receber os resultados da varredura do sonarqube via webhooks
#path('resultadosscan/', ResultadosScanAPIView.as_view(), name='resultadosscan'),
#path('resultadosscan/<int:pk>/', ResultadoScanAPIView.as_view(), name='resultadoscan'),
#path('resultadosscan/', ResultadosScanAPIView.as_view({'post': 'create'}), name='resultadosscan'),


# 3º passo: executar a varredura da aplicação
# print ("Executando o scan do projeto...")
# comando = "docker exec mn.sonar_cli bash -c 'sonar-scanner -X -Dsonar.projectKey=dvwa"
# comando = comando + f" -Dsonar.sources=app/DVWA -Dsonar.host.url={sonar_host} -Dsonar.token={sonar_dvwa_token}"
# comando = comando + f" -Dsonar.login=mmpinto -Dsonar.password=@dm1n'"
# print (f"Comando: {comando}")
# try:
#     stdin,stdout,stderr = ssh.exec_command(comando)
#     stdin.write('docker\n')
#     stdin.flush()    
#     stdin.close()
#     print(stdout.readlines())
#     if 'EXECUTION FAILURE' in stdout.readlines():
#         print("Erro na execução do comando!")   
#     elif 'ANALYSIS SUCCESSFUL' in stdout.readlines():
#         print("Análise realizada com sucesso!")
#     print(stderr.readlines())
# except paramiko.SSHException as e:
#     print(f'Erro ao executar o comando remoto: {e}')
# print()


#try:
#    container = cliente.containers.get('mn.sonar_cli')
#    print ("Comando de preparação executado com sucesso!!")
#except docker.errors.NotFound as e:
#    print(f'Erro ao acessar o servidor Docker: {e}')
#    ssh_result = execute_ssh(comando)
#    print ("Comando de preparação executado com sucesso!!")
#    print (ssh_result)

#nova_aplicacao = {
#   "nome": "Aplicação 3",
#   "descricao": "Descrição da aplicação 3",
#   "tipo": "1"
#   
#}

# fixando para acesso com autenticação via token de umm usuário específico
# token obtido no SonarQube, na aplicação dvwa
#headers = {'Authorization':'Token squ_0b2cafe9d40615f6ec9dbb3ba037085fd7019363'}

#print("Obtendo os status do SonarQube via API...")
#sonar = requests.get(f'{sonar_api}/system/status')
#print(sonar.status_code)
#print(sonar.json())
#print()

#print("Autenticando no SonarQube...")
# Autenticar no SonarQube com o usuário criado com perfil de administrador
#auth = ('mmpinto','@dm1n')  
#try:
#    sonar_auth = requests.post(f'{sonar_api}/authentication/login', data={'login':'mmpinto','password':'@dm1n'})
#    print(sonar_auth.status_code)    
#except Exception as e:
#    print(f'Erro ao autenticar no SonarQube: {e}')
#print()

# Verificar se a aplicação DVWA já está cadastrada no SonarQube
#nova_aplicacao = {
#   "name": "Damn Vulnerable Web Application",
#   "project": "dvwa"
#}
# Consultar a aplicação DVWA no sonarqube
#try:
#    applic = requests.get(f'{sonar_api}/projects/search',data={'q':'dvwa'})
#    print(applic.status_code)
#    #print(app.json())
#except Exception as e:
#    print(f'Não encontrou a aplicação: {e}')
    # incluir o projeto no sonar
#    try:
#        app = requests.post(f'{sonar_api}/projects/create', data=nova_aplicacao)
#        print(app.status_code)
#    except Exception as e:
#         print(f'Erro ao criar o projeto: {e}')
#print()

    
    #ssh_result = execute_ssh(comando)
    #print (ssh_result)
    #cliente = docker.DockerClient.from_env(base_url=docker_server, container='mn.sonar_cli', cmd=comando)   
    #try: 
    #   cont = cliente.containers.get ('mn.sonar_cli')   
    #   cliente ('mn.sonar_cli', comando)
    #except docker.errors.NotFound as e1:
    #    container = cliente.containers.get('mn.sonar_cli')
    #    container. (f'cd /app && rm -rf DVWA && git clone {dvwa_fonte}')
    #except docker.errors.APIError as e1:
    #   print(f'Erro ao acessar o servidor Docker: {e1}')
    
    #subprocess.run(comando, shell=False, check=True)
    #subprocess.run("ssh docker@192.168.0.15 docker exec -it mn.sonar_cli ls", shell=False, check=True)
    #comando = "ssh docker@192.168.0.15 docker exec -it mn.sonar_cli bash -c 'sonar-scanner -Dsonar.projectKey=dvwa"
#    comando = "ssh docker@192.168.0.9 docker exec -it mn.sonar_cli bash -c 'sonar-scanner -Dsonar.projectKey=dvwa"
#    comando = comando + f" -Dsonar.sources=DVWA -Dsonar.host.url={sonar_host} -Dsonar.token={sonar_dvwa_token}"
#    comando = comando + f" -Dsonar.login=mmpinto -Dsonar.password=@dm1n'"
#    print (comando)
    #ssh_result = execute_ssh(comando)
    
    #print (ssh_result)
    
 #   subprocess.run(comando, shell=True, check=True)
#except paramiko.SSHException as e:
#    print(f'Erro ao executar o comando via SSH: {e}')

#nova_aplicacao = {
#   "nome": "Aplicação 3",
#   "descricao": "Descrição da aplicação 3",
#   "tipo": "1"
#}

# buscar resultados de varredura
#print("Buscando resultados de varredura...")
#try:
#    resultado = requests.get(f"{sonar_api}/project_analyses/search?projetc=dvwa", headers=headers)  
#    print(resultado.status_code)
#except Exception as e:
#    print(f'Erro ao buscar resultados de varredura: {e}')

#acesso = ('mmpinto','@dm1n')
#resultado = requests.get(f"{sonar_api}/projects/dvwa/reports", auth=acesso ,headers=headers)  
#print(resultado.status_code)
#print(resultado.json())


#resultado = requests.post(url_base_aplicacoes, headers=headers, data=nova_aplicacao)  
#print(resultado.status_code)
#assert resultado.status_code == 201

#resultado = requests.post(url_base_aplicacoes, headers=headers, data=nova_aplicacao)  
#resultado = requests.post(url_base_aplicacoes, headers=headers, data=nova_aplicacao)  
#print(resultado.status_code)
##assert resultado.status_code == 201

# passos 
# 1º ) buscar as ferramentas de varredura que fazem SAST
# 2º ) buscar as versões da aplicação habilitadas para esse tipo de varredura
# 3º ) iniciar a varredura para cada versão da aplicação
# 4º ) obter os resultados da varredura
# 5º ) armazenar os resultados da varredura

#tipo_varredura = 'SAST'
#tipos_varredura = requests.get('http://locahost:8000/api/v2/tiposvarredura') #, headers=headers)  
#print(tipos_varredura.json())

#sistemas_varredura = requests.get(url_base_sistemas_varredura) #, headers=headers)
#print(sistemas_varredura.json())  


#versoes = requests.get('http://locahost:8000/api/v2/versoes/', headers=headers)

#print(versoes.json())  