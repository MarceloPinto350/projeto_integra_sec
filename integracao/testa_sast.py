import docker.errors
import requests,docker,subprocess
# fixando para acesso com autenticação via token de umm usuário específico
headers = {'Authorization':'Token f0ee4a32f947f00cc06202ee306b5524fe1f3590'}

url_base_aplicacoes = 'http://localhost:8000/api/v2/aplicacoes/'
url_base_versoes = 'http://localhost:8000/api/v2/versoes/'
sonar_api = 'http://192.168.0.3:9000/api'
docker_server = 'tcp://192.168.0.3:1081'

sonar = requests.get(f'{sonar_api}/system/status')
print(sonar.status_code)
print(sonar.json())
print("Autenticando no SonarQube...")
# Autenticar no SonarQube
try:
    sonar_auth = requests.post(f'{sonar_api}/authentication/login', data={'login':'admin','password':'@dm1n'})
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
    app = requests.get(f'{sonar_api}/projects/search',data={'projects':'dvwa'})
    print(app.json())
except Exception as e:
    print(f'Erro ao buscar a aplicação: {e}')
    # incluir o projeto no sonar
    try:
        app = requests.post(f'{sonar_api}/projects/create', data=nova_aplicacao)
        print(app.status_code)
    except Exception as e:
         print(f'Erro ao criar o projeto: {e}')
print()

# executar o scan do projeto via sonar_cli no container
try:
    #cliente_docker = docker.DockerClient(base_url=docker_server)
    #print(cliente_docker.containers.list())
    #sonar_cli = cliente_docker.containers.get('sonar_cli')
    #sonar_cli.run('sonar-scanner -Dsonar.projectKey=projeto1 -Dsonar.sources=. -Dsonar.host.url=http://localhost:9000 -Dsonar.login=3c3c7d7c4b6f8c5c8c6c5c4c5c6c8c5c7
    #print (sonar_cli.run('ps -ef'))
    comando = 'ssh docker@192.168.0.3 docker exec sonar_cli sonar-scanner -Dsonar.projectKey=dvwa -Dsonar.sources=. -Dsonar.host.url=http://192.168.0.3:9000 -Dsonar.token=squ_fea9f59e34e27c3d7283eb8d468d137440cdbaae'
    subprocess.run(comando, shell=True, check=True)
except docker.errors.DockerException as e:
    print(f'Erro ao acessar o servidor Docker: {e}')


nova_aplicacao = {
   "nome": "Aplicação 3",
   "descricao": "Descrição da aplicação 3",
   "tipo": "1"
   
}

#resultado = requests.post(url_base_aplicacoes, headers=headers, data=nova_aplicacao)  
#print(resultado.status_code)
#assert resultado.status_code == 201


#versoes = requests.get('http://locahost:8000/api/v2/versoes/', headers=headers)

#print(versoes.json())  