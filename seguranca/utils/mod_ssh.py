import paramiko
import paramiko.ssh_exception    
import json 
import logging

#from fabric import Connection,SerialGroup
#import requests, docker, subprocess, paramiko    # para acessar o servidor docker

# sonar_host = 'http://192.168.0.9:32768'
# sonar_api = f'{sonar_host}/api'
# docker_server = 'http://192.168.0.9:2375'
# dvwa_fonte = 'https://github.com/MarceloPinto350/DVWA.git'
# sonar_dvwa_token = 'squ_0b2cafe9d40615f6ec9dbb3ba037085fd7019363'   # mmpinto
#sonar_dvwa_token = 'sqp_bd4affac00ce57c87e24b65544df7bbe821c2235'   #admin

# configurar o log
logger = logging.getLogger(__name__)

# parâmetros de conexão SSH
ssh_connect = paramiko.SSHClient()
ssh_connect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                     
def conecta_ssh(host, usuario, senha):    
    try:
        ssh_connect.connect(hostname=host, username=usuario, password=senha)
        return True
    except paramiko.ssh_exception.AuthenticationException as e:
        #print(f'Erro ao conectar via SSH: {e}')
        logger.error(f'Erro ao autenticarno SSH: {e}')  
        return False
    except paramiko.ssh_exception.NoValidConnectionsError as e1:
        logger.error(f'Erro ao tentar conectar no SSH: {e1}')  
        return  False
    except paramiko.ssh_exception.SSHException as e2:
        logger.error(f'Erro ao tentar conectar no SSH: {e2}')  
        return  False

def exec_comando_ssh(comando):
    try:
        stdin,stdout,stderr = ssh_connect.exec_command(comando)
        stdin.write('docker\n')
        stdin.flush()    
        stdin.close()
        retorno = {
            "stdout": stdout.readlines(),
            "stderr": stderr.readlines()
        }
    except paramiko.SSHException as e:
        #print(f'Erro ao executar o comando remoto {comando}: {e}')
        logger.error(f'Erro ao executar o comando remoto {comando}: {e}')
        retorno = {
            "stdout": None,
            "stderr": None
        }
    return retorno

def retorna_stout_ssh(comando, tipo):
    try:
        stdin,stdout,stderr = ssh_connect.exec_command(comando)
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
    

def testa():
    if conecta_ssh('192.168.0.13', 'docker', 'docker'):
        resultado = exec_comando_ssh("docker inspect owasp_dc")  
        #for val in resultado["stdout"]:
        #    print(val)
        
        # localizar o valor do campo "Mountpoint" no resultado da inspeção do container (docker inspect owasp_dc)
        print(resultado["stdout"][5])
        # filtrar o valor do campo "Mountpoint" no resultado da inspeção do container (docker inspect owasp_dc)
        caminho = ((resultado["stdout"][5].split(':')[1].strip().replace('"','')).replace(',',''))+'/src/report'
        #print((resultado["stdout"][5].split(':')[1].strip().replace('"','')).replace(',',''))
        print(caminho)  
        
        resultado = exec_comando_ssh("docker exec mn.owasp_dc bash -c 'cat /src/report/dependency-check-report.json'")
        print(resultado.keys())     
        #print(resultado["stdout"][0])
        print("*-*-*-*-*")
        resultado = retorna_stout_ssh("docker exec mn.owasp_dc bash -c 'cat /src/report/dependency-check-report.json'", 'JSON')
        
        print (resultado.keys())
        print (resultado)
        #for valor in resultado.items[0].itens():
        #    print(valor[0])
        
    else: 
        print('Não foi possível conectar no docker via SSH')    

host='192.168.0.13'
comando = 'hostname'

print(f'Testando conexão SSH com o host {host}... {conecta_ssh(host,"docker","docker")}')
print(f"Testando execução de comando SSH no host {host}... {exec_comando_ssh('docker exec mn.owasp_dc uname -s')}")

#print('---')
#host='192.168.0.19'

#print(f'Testando conexão SSH com o host {host}... {conecta_ssh(host,"docker","docker")}')
#print(f'Testando execução de comando SSH no host {host}... {exec_comando_ssh(comando)}')      

print('--- ----')
testa()

ssh_connect.close()


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