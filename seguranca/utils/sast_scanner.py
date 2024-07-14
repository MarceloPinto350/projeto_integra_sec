# Description: Este módulo contém as funções para iniciar e obter os resultados das varreduras de segurança.
import requests, docker 

# importar as bibliotecas para as ferramentas de segurança
#import sonarQube
#import owaspZap


# Define o métodos para iniciar e obter os resultados da varredura para o SonarQube
def sonarQube_scan(ferramenta_url, aplicacao):
    #headers = {'Authorization':'Token f0ee4a32f947f00cc06202ee306b5524fe1f3590'}
    headers = {''}
    url_login = f"{ferramenta_url}/api/authentication/login"
    url_projetos = f"{ferramenta_url}/api/projects/search"

    login = {
        "login": "admin",
        "password": "@dm1n"
    }
    # efetiva o o login no sonarQube
    resultado = requests.post(url_login, headers=headers, data=login)  
    # validar se autenticou corretamente
    print(resultado.status_code)
    #assert resultado.status_code == 201
    
    # Conectar ao SonarQube via CLI /api/authentication/login
    projeto = requests.get(url_projetos, headers=headers, data=f"projects=[{aplicacao}]")
    print(projeto.json())
    
    sonar_cli =   docker.from_env()
    
    

   # Iniciar a varredura
   #project_key = sonarQube_client.create_project(application_url, application_name)
   #sonarQube_client.analyze_project(project_key, code_source_url)

   # Obter os resultados da varredura
   #results = sonarQube_client.get_issues(project_key)
   #return results


# Define o método para iniciar e obter os resultados da varredura para o OWASP ZAP
#def owaspZap_scan(application_url):
    # Iniciar o OWASP ZAP
#    zap = owaspZap.Zap()
#    zap.start()

    # Adicionar a URL da aplicação à lista de alvos
#    zap.spider(application_url)

    # Executar a varredura

def busca_tipos_varredura(tipo_varredura):
    # para acesso com autenticação via token
    headers = {'Authorization':'Token f0ee4a32f947f00cc06202ee306b5524fe1f3590'}

    # Obter o ID da varredura do tipo passado como parâmetro
    tipos = requests.get('http://locahost:8000/api/v2/tiposvarredura/', headers=headers)
    for tipo in tipos.json():
        if tipo['sistemas_varredura'][0] == tipo_varredura:
            return tipo['id']

    #sonarQube_results = sonarQube_scan('http://localhost:8000', '/appseg')
    #print(sonarQube_results)

    # Obter as varreduras do OWASP ZAP
    #owaspZap_results = owaspZap_scan('http://localhost:8000')
    #print(owaspZap_results)
    