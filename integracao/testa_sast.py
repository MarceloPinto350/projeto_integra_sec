import docker.errors
import requests,docker,subprocess
import requests #, seguranca.sast_scanner
import paramiko    # para acessar o servidor docker
#from docker import DockerClient
# fixando para acesso com autenticação via token de umm usuário específico
headers = {'Authorization':'Token squ_0b2cafe9d40615f6ec9dbb3ba037085fd7019363'}

url_base_aplicacoes = 'http://localhost:8000/api/v2/aplicacoes/'
url_base_versoes = 'http://localhost:8000/api/v2/versoes/'
url_base_sistemas_varredura = 'http://localhost:8000/api/v2/sistemasvarredura/'

sonar_host = 'http://192.168.0.9:32768'
sonar_api = f'{sonar_host}/api'
docker_server = 'tcp://192.168.0.9:1081'
dvwa_fonte = 'https://github.com/digininja/DVWA.git'
sonar_dvwa_token = 'squ_0b2cafe9d40615f6ec9dbb3ba037085fd7019363'   # mmpinto
#sonar_dvwa_token = 'sqp_bd4affac00ce57c87e24b65544df7bbe821c2235'   #admin

nova_aplicacao = {
   "nome": "Aplicação 3",
   "descricao": "Descrição da aplicação 3",
   "tipo": "1"
   
}

sonar = requests.get(f'{sonar_api}/system/status')
print(sonar.status_code)
print(sonar.json())
print("Autenticando no SonarQube...")
# Autenticar no SonarQube
try:
    sonar_auth = requests.post(f'{sonar_api}/authentication/login', data={'login':'mmpinto','password':'@dm1n'})
    print(sonar_auth.status_code)
    print('Autenticado!')
except Exception as e:
    print(f'Erro ao autenticar no SonarQube: {e}')
print()

# Verificar se a aplicação DVWA já está cadastrada no SonarQube
nova_aplicacao = {
   "name": "Damn Vulnerable Web Application",
   "project": "dvwa"
}
try:
    app = requests.get(f'{sonar_api}/projects/search',data={'q':'dvwa'})
    print(app.json())
except Exception as e:
    print(f'Não encontrou a aplicação: {e}')
    # incluir o projeto no sonar
#    try:
#        app = requests.post(f'{sonar_api}/projects/create', data=nova_aplicacao)
#        print(app.status_code)
#    except Exception as e:
#         print(f'Erro ao criar o projeto: {e}')
print()

# define a conexão SSH
ssh = paramiko.SSHClient()
def execute_ssh (comando):
   ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   ssh.connect(hostname='192.168.0.9', username='docker', password='docker')
   stdin,stdout,stderr = ssh.exec_command(comando)
   stdin.close()
   result = stdout.read()
   return result 

# executar o scan do projeto via sonar_cli no container
print("Executando teste do ssh...")
try:
    ssh_result = execute_ssh("docker ps")
    print (ssh_result)
except paramiko.SSHException as e:
    print(f'Erro ao executar o comando via SSH: {e}')
print()


# executar o scan do projeto via sonar_cli no container
#comando = f"ssh docker@192.168.0.15 docker exec -it mn.sonar_cli bash -c 'cd /app && rm -rf DVWA && git clone {dvwa_fonte}'"
comando = f"docker exec -it mn.sonar_cli bash -c 'cd /app && rm -rf DVWA && git clone {dvwa_fonte}'"
#comando = f'cd /app && rm -rf DVWA && git clone {dvwa_fonte}'
print ("preparando dados para o comando remoto...")
try:
    ssh_result = execute_ssh(comando)
    ssh_result = execute_ssh('docker sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
    print (ssh_result)
except paramiko.SSHException as e:
    print(f'Erro ao executar o comando remoto: {e}')
print()

#try:
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


nova_aplicacao = {
   "nome": "Aplicação 3",
   "descricao": "Descrição da aplicação 3",
   "tipo": "1"
   
}

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