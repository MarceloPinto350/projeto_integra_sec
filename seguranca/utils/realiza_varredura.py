import requests, json


headears = {'Authorization':'Token 61a384f801cb080e0c8f975c7731443b51c9f02e'}
url_base = 'http://192.168.0.22:8000/api/v2/'

# método para buscar os tipos de varredura da aplicação
def get_sistemas_varredura(aplicacao_id):
    """
    Retorna os sistemas de varredura habilitados para a aplicação passada como parâmetro
    """
    # obtem a aplicação
    aplicacao = requests.get(f'{url_base}/{aplicacao_id}') #, headers=headears)
    if aplicacao.status_code == 200:
        # obtem os sistemas de varredura habilitados para a aplicação
        sistemas_varredura = aplicacao.json().get('sistemas_varredura')
        return (sistemas_varredura)
    else:
        return (aplicacao.status_code)
    
# métodos para processar a varredura do SonarQube
def sonarQube_scan(ferramenta_url, aplicacao):
    """
    Conecta ao Sonar-CLI e inicia a varredura da aplicação

    Args:
        ferramenta_url (_type_): _description_
        aplicacao (_type_): _description_
        
    """
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
    
    #sonar_cli =   docker.from_env()
    return()
    
    

   # Iniciar a varredura
   #project_key = sonarQube_client.create_project(application_url, application_name)
   #sonarQube_client.analyze_project(project_key, code_source_url)

   # Obter os resultados da varredura
   #results = sonarQube_client.get_issues(project_key)
   #return results

#método para processar a varredura do Owasp dependency-check
def owaspDC_scan(ferramenta_url, aplicacao):
    """_summary_

    Args:
        ferramenta_url (_type_): _description_
        aplicacao (_type_): _description_

    Returns:
        _type_: _description_
    """
    return ()

# método para iniciar e obter os resultados da varredura para o OWASP ZAP
def owaspZap_scan(ferramenta_url, aplicacao):
    """Conecta ao owasp-zap e inicia a varredura da aplicação

    Args:
        ferramenta_url (_type_): _description_
        aplicacao (_type_): _description_
    """
    # Iniciar o OWASP ZAP
#    zap = owaspZap.Zap()
#    zap.start()

    # Adicionar a URL da aplicação à lista de alvos
#    zap.spider(application_url)

    # Executar a varredura
    return (rai)
    
# método que inicia a análise e processa a varredura da aplicação, conforme o caso
def inicializalizacao():
    """
    Inicializa as variáveis de ambiente
    """
    # inicializa as variáveis de ambiente
    sonarQube_url = 'http:// '   
    return ()