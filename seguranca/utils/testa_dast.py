import requests, paramiko, io, logging     # para acessar o servidor docker
from rest_framework.response import Response

# importando o serializer para salvar os dados no BD
#from seguranca.serializers import ResultadoScanSerializer
#from utils import varredura_result
import varredura_result

logger = logging.getLogger(__name__)

docker_host = '192.168.0.12'
sonar_host = 'http://192.168.0.12:32768'
sonar_api = f'{sonar_host}/api'
docker_server = 'http://192.168.0.12:2375'
dvwa_fonte = 'https://github.com/MarceloPinto350/DVWA.git'
sonar_dvwa_token = 'squ_0b2cafe9d40615f6ec9dbb3ba037085fd7019363'   # mmpinto
#sonar_dvwa_token = 'sqp_bd4affac00ce57c87e24b65544df7bbe821c2235'   #admin
#NVD API Key: 480fab96-3816-4ea8-be1f-cce19cdf026d  

# define a conexão SSH
ssh = paramiko.SSHClient()
#def execute_ssh (comando):
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=docker_host, username='docker', password='docker')

output = "owasp_zap_report.xml"

# template do script para autenticação
# // This authentication script can be used to authenticate in a webapplication via forms.
# // The submit target for the form, the name of the username field, the name of the password field
# // and, optionally, any extra POST Data fields need to be specified after loading the script.
# // The username and the password need to be configured when creating any Users.

# // The authenticate function is called whenever ZAP requires to authenticate, for a Context for which this script
# // was selected as the Authentication Method. The function should send any messages that are required to do the authentication
# // and should return a message with an authenticated response so the calling method.
# //
# // NOTE: Any message sent in the function should be obtained using the 'helper.prepareMessage()' method.
# //
# // Parameters:
# //		helper - a helper class providing useful methods: prepareMessage(), sendAndReceive(msg)
# //		paramsValues - the values of the parameters configured in the Session Properties -> Authentication panel.
# //					The paramsValues is a map, having as keys the parameters names (as returned by the getRequiredParamsNames()
# //					and getOptionalParamsNames() functions below)
# //		credentials - an object containing the credentials values, as configured in the Session Properties -> Users panel.
# //					The credential values can be obtained via calls to the getParam(paramName) method. The param names are the ones
# //					returned by the getCredentialsParamsNames() below

# function authenticate(helper, paramsValues, credentials) {
# 	print("Authenticating via JavaScript script...");

# 	// Make sure any Java classes used explicitly are imported
# 	var HttpRequestHeader = Java.type("org.parosproxy.paros.network.HttpRequestHeader")
# 	var HttpHeader = Java.type("org.parosproxy.paros.network.HttpHeader")
# 	var URI = Java.type("org.apache.commons.httpclient.URI")

# 	// Prepare the login request details
# 	var requestUri = new URI(paramsValues.get("Target URL"), false);
# 	var requestMethod = HttpRequestHeader.POST;
	
# 	// Build the request body using the credentials values
# 	var extraPostData = paramsValues.get("Extra POST data");
# 	var requestBody = paramsValues.get("Username field") + "=" + encodeURIComponent(credentials.getParam("Username"));
# 	requestBody+= "&" + paramsValues.get("Password field") + "=" + encodeURIComponent(credentials.getParam("Password"));
# 	if(extraPostData.trim().length() > 0)
# 		requestBody += "&" + extraPostData.trim();

# 	// Build the actual message to be sent
# 	print("Sending " + requestMethod + " request to " + requestUri + " with body: " + requestBody);
# 	var msg = helper.prepareMessage();
# 	msg.setRequestHeader(new HttpRequestHeader(requestMethod, requestUri, HttpHeader.HTTP10));
# 	msg.setRequestBody(requestBody);
# 	msg.getRequestHeader().setContentLength(msg.getRequestBody().length());

# 	// Send the authentication message and return it
# 	helper.sendAndReceive(msg);
# 	print("Received response status code: " + msg.getResponseHeader().getStatusCode());

# 	return msg;
# }

# // This function is called during the script loading to obtain a list of the names of the required configuration parameters,
# // that will be shown in the Session Properties -> Authentication panel for configuration. They can be used
# // to input dynamic data into the script, from the user interface (e.g. a login URL, name of POST parameters etc.)
# function getRequiredParamsNames(){
# 	return ["Target URL", "Username field", "Password field"];
# }

# // This function is called during the script loading to obtain a list of the names of the optional configuration parameters,
# // that will be shown in the Session Properties -> Authentication panel for configuration. They can be used
# // to input dynamic data into the script, from the user interface (e.g. a login URL, name of POST parameters etc.)
# function getOptionalParamsNames(){
# 	return ["Extra POST data"];
# }

# // This function is called during the script loading to obtain a list of the names of the parameters that are required,
# // as credentials, for each User configured corresponding to an Authentication using this script 
# function getCredentialsParamsNames(){
# 	return ["Username", "Password"];
# }



def prepara_varredura():
    """
    Função que faz a criação do arquivo de configuração para o processamento da varredura DAST
    """
    # 1º passo: criar o script de autenticação para a aplicação com usuário e senha
    script_js = """function authenticate(helper, paramsValues, credentials) {
        print("Authenticating via JavaScript script...");
        // Make sure any Java classes used explicitly are imported
        var HttpRequestHeader = Java.type("org.parosproxy.paros.network.HttpRequestHeader")
        var HttpHeader = Java.type("org.parosproxy.paros.network.HttpHeader")
        var URI = Java.type("org.apache.commons.httpclient.URI")
        
        // Prepare the login request details
        var requestUri = new URI(paramsValues.get("Target URL"), false);
        var requestMethod = HttpRequestHeader.POST;
	
	    // Build the request body using the credentials values
        var extraPostData = paramsValues.get("Extra POST data");
        var requestBody = paramsValues.get("Username field") + "=" + encodeURIComponent(credentials.getParam("Username"));
        requestBody+= "&" + paramsValues.get("Password field") + "=" + encodeURIComponent(credentials.getParam("Password"));
        
        if(extraPostData.trim().length() > 0)
            requestBody += "&" + extraPostData.trim();

    	// Build the actual message to be sent
        print("Sending " + requestMethod + " request to " + requestUri + " with body: " + requestBody);
        var msg = helper.prepareMessage();
        msg.setRequestHeader(new HttpRequestHeader(requestMethod, requestUri, HttpHeader.HTTP10));
        msg.setRequestBody(requestBody);
        msg.getRequestHeader().setContentLength(msg.getRequestBody().length());

    	// Send the authentication message and return it
        helper.sendAndReceive(msg);
        print("Received response status code: " + msg.getResponseHeader().getStatusCode());

	    return msg;
    }
    
    function getRequiredParamsNames(){
        return ["Target URL", "Username field", "Password field"];
    }

    function getOptionalParamsNames(){
        return ["Extra POST data"];
    }

    function getCredentialsParamsNames(){
        return ["Username", "Password"];
    }
    """
    
    # Cria um objeto para armazenar o conteúdo do arquivo
    sftp = ssh.open_sftp()

    # Se o conteúdo for fornecido, cria um arquivo em memória
    if script_js:
        arquivo = io.BytesIO(script_js.encode('utf-8'))
    
    # Transfere o arquivo para o servidor remoto
    print ("Criando o script...")
    #print (f"Direttório remoto: {sftp.listdir()}")
    print (f"Comando: sftp.putfo(arquivo, '/var/lib/docker/volumes/owasp_zap/_data/authentication.js')")
    try:
        sftp.putfo(arquivo, "/var/lib/docker/volumes/owasp_zap/_data/authentication.js")
    except paramiko.SSHException as e:
        print(f'Erro ao criar o arquivo remoto: {e}')
        logger.error (f'Erro ao criar o arquivo remoto: {e}')
    except PermissionError as ee:
        print(f'Erro ao criar o arquivo remoto: {ee}')
        logger.error (f'Erro ao criar o arquivo remoto: {ee}')
    except IOError as eee:
        print(f'Erro ao criar o arquivo remoto: {eee}')
        logger.error (f'Erro ao criar o arquivo remoto: {eee}')

    # Fecha a conexão
    sftp.close()
    
    # comando = f"docker exec mn.owasp_dc bash -c 'echo ''{script}'' > scripts/authentication.js'\n"
    # print ("Criando o script...")
    # print (f"Comando: {comando}")        
    # try:  
    #     stdin,stdout,stderr = ssh.exec_command(comando)
    #     stdin.write('docker\n')
    #     stdin.flush()    
    #     stdin.close()
    #     print(f"stdout: {stdout.readlines()}")
    #     print(f"stderr: {stderr.readlines()}")    
    # except paramiko.SSHException as e:
    #     print(f'Erro ao executar o comando remoto: {e}')
    #     logger.error (f'Erro ao executar o comando remoto: {e}')    
    print('-')

def executa_varredura():
    """
    Função que executa a varredura DAST
    """
    # 2ª passo: rodar o scanner do owasp-zap via CLI
    url_zap = "http://192.168.0.12:32770/"
    comando = f"docker exec mn.owasp_zap bash -c 'zap.sh -dir wrk -loglevel ERROR -script script/authentication.js -cmd -quickurl {url_zap} -quickprogress -quickout {output}'\n"
    #comando = f"docker exec mn.owasp_zap bash -c 'zap.sh -dir wrk -loglevel ERROR -cmd -quickurl {url_zap} -quickprogress -quickout {output}'\n"
    print ("Executando a varredura...")
    print (f"Comando: {comando}")            
    try:
        stdin,stdout,stderr = ssh.exec_command(comando)
        stdin.write('docker\n')
        stdin.flush()    
        stdin.close()
        print(f"stdout: {stdout.readlines()}")
        print(f"stderr: {stderr.readlines()}")    
    except paramiko.SSHException as e:
        print(f'Erro ao executar o comando remoto: {e}')
        logger.error (f'Erro ao executar o comando remoto: {e}')
    print('--')

def coleta_resultado():
    """
    Função que coleta o resultado da varredura DAST
    """
    # 3º passo: coletar o resultado da varredura
    comando = f"docker exec mn.owasp_dc cat /wrk/{output}"
    print(comando)
    try:
        stdin,stdout,stderr = ssh.exec_command(comando)
        stdin.write('docker\n')
        stdin.flush()    
        stdin.close()
        #print(f"stdout: {stdout.readlines()}")
        print(f"stderr: {stderr.readlines()}")    
        #print(stderr.channel.recv_exit_status() == 0)
        if stderr.channel.recv_exit_status() == 0: # testar se não retornou erro
            print("Arquivo encontrado com sucesso!")
            data = stdout.readlines()
            print (data)
            print ("------------------------------------")
            #converter o arquivo XML para JSON
            dados = data.xml_to_json()
            print (dados)
            #dados = varredura_result.xml_to_json(data)
            #payload = json.dumps(dados,indent=3)
            #print (payload)
            
            # validar o serializer e salvar dados no BD
            #headers = {'Content-Type': 'application/json'}
            #response = requests.post('http://192.168.0.22:8000/api/v1/resultados/',data=payload, headers=headers)
            #if response.status_code == 201:
            #    print("Dados inseridos no BD!")
            #else:
            #    print("Erro ao enviar os dados para gravação no BD:", response.status_code)
            # logger.error (f'Erro ao salvar os dados no BD: {response.text}')
            
    except paramiko.SSHException as e:
        print(f'Erro ao executar o comando remoto: {e}')
        logger.error (f'Erro ao executar o comando remoto: {e}')    
    print('---')

# processando os testes
prepara_varredura()
executa_varredura()
coleta_resultado()
ssh.close()





# # 3º passo: coletar o resultado da varredura
# comando = "docker inspect owasp_dc"
# print(comando)
# try:
#     stdin,stdout,stderr = ssh.exec_command(comando)
#     stdin.write('docker\n')
#     stdin.flush()    
#     stdin.close()
#     print(f"stdout: {stdout.readlines()}")
#     print(f"stderr: {stderr.readlines()}")    
#     if 'owasp_dc' in stdout.readlines():
#         print("Análise realizada com sucesso!")
#         dados = json.loads(stdout.readlines())
#         print(dados['Mounts'][0]['Source'] + '/report/dependency-check-report.json')
# except paramiko.SSHException as e:
#     print(f'Erro ao executar o comando remoto: {e}')
#     logger.error (f'Erro ao executar o comando remoto: {e}')    
# print('---')


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
    #subprocess.run("ssh docker@192.168.0.12 docker exec -it mn.sonar_cli ls", shell=False, check=True)
    #comando = "ssh docker@192.168.0.12 docker exec -it mn.sonar_cli bash -c 'sonar-scanner -Dsonar.projectKey=dvwa"
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




