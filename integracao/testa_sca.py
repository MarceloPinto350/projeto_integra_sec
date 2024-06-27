import requests, docker, subprocess, paramiko,json     # para acessar o servidor docker
#from docker import DockerClient

#url_base_aplicacoes = 'http://localhost:8000/api/v2/aplicacoes/'
#url_base_versoes = 'http://localhost:8000/api/v2/versoes/'
#url_base_sistemas_varredura = 'http://localhost:8000/api/v2/sistemasvarredura/'

sonar_host = 'http://192.168.0.9:32768'
sonar_api = f'{sonar_host}/api'
docker_server = 'http://192.168.0.9:2375'
dvwa_fonte = 'https://github.com/MarceloPinto350/DVWA.git'
sonar_dvwa_token = 'squ_0b2cafe9d40615f6ec9dbb3ba037085fd7019363'   # mmpinto
#sonar_dvwa_token = 'sqp_bd4affac00ce57c87e24b65544df7bbe821c2235'   #admin

# executar teste no servidor docker via SSH
#print("Executando teste do ssh no servidor docker...")
#try:
#    ssh_result = execute_ssh("docker ps")
#    if "sonar_cli" in str(ssh_result):
#        print("Container sonar_cli encontrado!")
#    else:
#        print("Container sonar_cli não encontrado!")
#except paramiko.SSHException as e:
#    print(f'Erro ao executar o comando via SSH: {e}')
#print()

# criar uma configuração para acesso ao docker pelo próprio python
# Definida a variável de ambiente antes de chamar o cliente DOCKER_HOST=tcp://1920  
#print("Conectando ao servidor Docker pelo próprio Python...")
#cliente = docker.from_env()
#cliente = docker.DockerClient(base_url=docker_server)
#try:
#    for container in cliente.containers.list():
#        print(container.name)
#except docker.errors.APIError as e:
#    print(f'Erro ao acessar o servidor Docker: {e}')   
#print()

#try:
#    cliente = docker.from_env()
#    print("Conexão com o servidor Docker realizada com sucesso!!")
#except docker.errors.APIError as e:
#    print(f'Erro ao acessar o servidor Docker: {e}')
#print(f"Versão da API: {cliente.api_version}") 
#print(cliente.info.())   

#resposta = requests.post(f'{docker_server}/v1.24/auth',
#            data={'username':'docker','password':'docker','serveraddress':{docker_server}})  
#print(resposta.status_code)

#resposta = requests.get(f'http://192.168.0.9:2375/v1.24/containers/json?all=1')
#print(resposta.status_code)

#print(cliente.containers.list(filters='name=mn.sonar_cli'))

# define a conexão SSH
ssh = paramiko.SSHClient()
#def execute_ssh (comando):
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='192.168.0.9', username='docker', password='docker')


# 1º passo: clonar na máquina do OWASP-DC a imagem da aplicação a ser varrida
comando = f"docker exec mn.owasp_dc bash -c 'cd /src && rm -rf DVWA && rm -f dependency-check-report.json && git clone {dvwa_fonte}'\n"
print ("Preparando para varredura...")
print (f"Comando: {comando}")        
try:  
    stdin,stdout,stderr = ssh.exec_command(comando)
    stdin.write('docker\n')
    stdin.flush()    
    stdin.close()
    print(stdout.readlines())
    print(stderr.readlines())    
    if "err" in stderr.readlines():
        print("Erro ao clonar o repositório!")
    else:
        print("Repositório clonado com sucesso!")
except paramiko.SSHException as e:
    print(f'Erro ao executar o comando remoto: {e}')
print()

# 2ª passo: criado webservice para receber os resultados da varredura do sonarqube via webhooks
comando = "docker exec mn.owasp_dc bash -c '/bin/dependency-check.sh --scan /src/DVWA --format JSON --out /src/report"
comando = f"{comando} --nvdApiKey cd0c05ca-2b15-4034-9ae6-490fb505f439'"
print("Executando o scan do projeto...")
print(comando)
try:
    stdin,stdout,stderr = ssh.exec_command(comando)
    stdin.write('docker\n')
    stdin.flush()    
    stdin.close()
    print(stdout.readlines())
    if 'Analysis Complete' in stdout.readlines():
        print("Análise realizada com sucesso!")        
    else:
        print("Erro na execução do comando!")   
    print(stderr.readlines())
except paramiko.SSHException as e:
    print(f'Erro ao executar o comando remoto: {e}')
print()

# 3º passo: coletar o resultado da varredura
comando = "docker inspect volume owasp_dc"
print(comando)
try:
    stdin,stdout,stderr = ssh.exec_command(comando)
    stdin.write('docker\n')
    stdin.flush()    
    stdin.close()
    print(stdout.readlines())
    if 'owasp_dc' in stdout.readlines():
        print("Análise realizada com sucesso!")
        dados = json.loads(stdout.readlines())
        print(dados['Mounts'][0]['Source'] + '/report/dependency-check-report.json')
        #relatorio = dados['Mounts'][0]['Source'] + '/report/dependency-check-report.json'
    elif 'Error' in stdout.readlines():
        print("Erro na execução do comando!")   
    print(stderr.readlines())
except paramiko.SSHException as e:
    print(f'Erro ao executar o comando remoto: {e}')
print()

#sftp = ssh.open_sftp()
#with sftp.open('/src/report/dependency-check-report.json','r') as arq:
#    dados_json = arq.read()
    
#dados = json.loads(dados_json)
#print(dados)

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