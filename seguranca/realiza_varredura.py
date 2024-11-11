import requests, json, logging, datetime, paramiko


from .models import Aplicacao, SistemaVarredura,VersaoAplicacao,TipoVarredura

url_base = 'http://127.0.0.1:8000/api/v2'
headers = {'Content-Type': 'application/json'}
    
# método que inicia a análise e processa a varredura da aplicação, conforme o caso
def inicializa(processar):
    """
    Inicializar as variáveis de ambiente
    Recebe os dados passados através de um JSON para processar a varredura da aplicação
    processar={
      "nome_aplicacao": "DVWA",
      "origem_processamento": "API",
      "sistema_varredura": ["ALL","SAST","DAST","SCA"]
      }
    """
    logger = logging.getLogger(__name__)
    
    try:
        nomeApp = processar['nome_aplicacao']
        origem = processar['origem_processamento']
        sistema = processar['sistema_varredura']
    except KeyError:
        msg = "Erro na estrtura do JSON encaminhado."
        print (msg)
        return ({"mensagem": msg})
    
    #registrando o inicio do processamento...
    dth_inicio = datetime.datetime.now()
    logger.info(f"Iniciando o processamento da varredura da aplicação {nomeApp}...")
    
    # buscar Dados da aplicação
    apps = Aplicacao.objects.get(sigla=nomeApp)
    logger.info(f"Aplicação a ser verificada: {apps.id}, {apps.nome}, {nomeApp}, {apps.url_codigo_fonte}")
    logger.info("Parâmetros de processamento: {processar}")
    print (f"Aplicação a ser verificada: {apps.id}, {apps.nome}, {nomeApp}, {apps.url_codigo_fonte}")
    
    # buscar os tipos de varreduras habilitados para a aplicação
    #print (sistema)
    if  "ALL" in sistema:
        tipos_varredura = TipoVarredura.objects.all()
    else:    
        tipos_varredura = TipoVarredura.objects.filter(nome__in=sistema)
        
    # buscar os sistemas de varredura habilitados para a aplicação
    sistemas_varredura = SistemaVarredura.objects.filter(situacao='ATIVO')
    lista_sistemas = []
    for sist_varr in sistemas_varredura:
        # pega a lista de versões da aplicação vinculadas ao sistema de varredura
        lista = sist_varr.aplicacoes.all()
        for appx in lista:
            # pega a aplicação da versão
            Vapp = VersaoAplicacao.objects.get(id=appx.id)
            if Vapp.aplicacao.id == apps.id:
                # adiciona a lista de sistemas de varredura habilitados para a aplicação
                lista_sistemas.append(sist_varr.aplicacao_seguranca.id)
    print (f"Lista de sistemas de varredura habilitados para aplicação: {lista_sistemas}")
    
    # gera a configuração da varredura
    dth_termino = datetime.datetime.now()
    varredura = {
        "origem": origem,
        "data_inicio": dth_inicio,
        "data_fim": dth_termino,
        "situacao": 'EM ANDAMENTO', # FALHA|EM ANDAMENTO|CONCLUÍDA
        "aplicacao": apps.id,
        "log": None,
    }
    # url_varredura = url_base + '/varreduras/'
    # print (f"Para gravação da varredura: {url_varredura} - {varredura}")  
    # try:
    #     response = requests.post(url_varredura,data=varredura, headers=headers)
    #     varredura_resp = response.json()
    #     print (varredura_resp.get('id'))
    # except requests.exceptions.RequestException as e:
    #     if response.status_code == 201:
    #         logger.info (f"Resultado da análise {processar.aplicacao_sigla}-{processar.sist_varredura_sigla_tipo}.{processar.varredura} inserida no BD.")
    #     else:
    #         print("Erro ao enviar os dados para gravação no BD:", response.status_code)
    #         logger.error (f"Erro ao salvar os dados no BD: {response.text}")           
    # # gera os resultados para a varredura
    # for tva in tipos_varredura:
    #     print (f"Tipo de varredura selecionada para processamento: {tva.id}, {tva.nome}, {tva.descricao}")
    #     # pegas os dados da configuração para executar o processamento
    #     sistema_varredura = SistemaVarredura.objects.filter(id__in=lista_sistemas, tipo_varredura=tva.id)
    #     for sv in sistema_varredura:
    #         # insere o resgistro da varredura 
    #         ########################################################
    #         # Resultados       
    #         #aplicacao = Aplicacao.objects.get(pk=serializer.data['aplicacao'])
    #         # coleta os sistemas de varredura ativos para a aplicação
    #         #print (f"Varrendo aplicação {serializer.data['aplicacao']}")
    #         print (f"Varrendo aplicação {apps}")
    #         #sistemas_varredura = SistemaVarredura.objects.filter(situacao='ATIVO', aplicacoes__in=serializer.data['aplicacao'])
    #         sistemas_varredura = SistemaVarredura.objects.filter(situacao='ATIVO', aplicacoes__in=apps)
    #         for sist_varr in sistemas_varredura:
    #             tipo_varr = TipoVarredura.objects.get(id=sist_varr.aplicacao_seguranca.id)
    #             if "SAST" == tipo_varr.nome:
    #                 processar = {
    #                     #"aplicacao": aplicacao.nome,
    #                     #"aplicacao_sigla": aplicacao.sigla,     
    #                     #"aplicacao_id": aplicacao.id,
    #                     #"url_codigo_fonte": aplicacao.url_codigo_fonte,
    #                     "aplicacao": apps.nome,
    #                     "aplicacao_sigla": apps.sigla,     
    #                     "aplicacao_id": apps.id,
    #                     "url_codigo_fonte": apps.url_codigo_fonte,
    #                     #"varredura": serializer.data['id'],
    #                     "varredura": varredura_resp['id'],
    #                     "sistema_varredura": sist_varr.id,
    #                     "sist_varredura_ip_acesso": sist_varr.ip_acesso,
    #                     "sist_varredura_comando": sist_varr.comando,
    #                     "sist_varredura_webhook": sist_varr.usa_webhook,
    #                     "sist_varredura_tipo": sist_varr.tipo_varredura,
    #                     "sist_varredura_sigla_tipo": "SAST",
    #                     "sist_varredura_usuario": sist_varr.usuario,
    #                     "sist_varredura_senha": sist_varr.senha,
    #                     "sist_varredura_token": sist_varr.token_acesso,
    #                     #"caminho_resultado": f"app/{aplicacao.sigla}_{sist_varr.sigla}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    #                     "caminho_resultado": f"app/{apps.sigla}_{sist_varr.sigla}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json",
    #                 }
    #                 # processo a varredura e retorna o resultado
    #                 # resultado = {
    #                 #    "aplicacao": aplicacao.pk,
    #                 #    "varredura": ultima_versao.nome_versao,
    #                 #    "sistemas_varredura": lista_sistemas
    #                 # }   
    #                 # realiza a varredura
    #                 print (f"Vai processar: {processar}")
    #                 #resultado = varrer_SAST.processa(processar)
    #                 resultado = varrer_SAST(processar)
    #                 print(resultado)
    #                 # validar o serializer e salvar dados no BD
    #                 #serializer =  ResultadoScanSerializer(data=resultado)
    #                 #if serializer.is_valid():
    #                 #serializer.save()
    #                 #return Response(serializer.data, status=201)
    #                 #else:
    #                 #return Response(serializer.errors, status=400)            
                
    # #print(varredura)       
    logger.info(f"Gravando a varredura para aplicação: {varredura}")    
    return (varredura)


def varrer_SAST (processar):
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
      "sist_varredura_comando": sist_varr.comando,
      "sist_varredura_webhook": sist_varr.usa_webhook,
      "sist_varredura_tipo": sist_varr.tipo_varredura,
      "sist_varredura_sigla_tipo": "SAST",
      "sist_varredura_usuario": sist_varr.usuario,
      "sist_varredura_senha": sist_varr.senha,
      "sist_varredura_token": sist_varr.token_acesso",
      "caminho_resultado": f"{aplicacao.sigla}_{sist_varredura.sigla}_{datetime.now().strftime('%Y%m%d%H%M%S")}.json"
    }
    """
    # define a conexão SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # baixar o código fonte da aplicação
        #ssh.connect(hostname='192.168.0.10', username='docker', password='docker")
        ssh.connect(hostname=processar.sist_varredura_ip_acesso, username=processar.sist_varredura_usuario, password=processar.sist_varredura_senha)
        # 1º passo: clonar na máquina do Sonar_CLI a imagem da aplicação a ser varrida
        #comando = f"docker exec mn.sonar_cli bash -c 'cd app && rm -rf DVWA && git clone {dvwa_fonte}'\n"
        # deve rodar o comando na máquina do sonar_cli na pasta app
        comando = f"docker exec mn.sonar_cli bash -c 'cd app && rm -rf {processar.aplicacao_sigla} && git clone {processar.url_codigo_fonte}'\n"
        print ("Preparando para varredura...")
        print (f"Comando: {comando}")        
        try:  
            stdin,stdout,stderr = ssh.exec_command(comando)
            stdin.write("docker\n")
            stdin.flush()    
            stdin.close()
            if stderr.readlines() != "[]":
                logger.error (stderr.readlines())
            else:
                logger.info (stdout.readlines())    
        except paramiko.SSHException as e:
            print(f"Erro ao executar o comando remoto: {e}")
            logger.error (f"Erro ao executar o comando remoto: {e}")  
        # 2º passo: executar a varredura da aplicação
        # comando = "docker exec mn.sonar_cli bash -c 'sonar-scanner -X -Dsonar.projectKey=dvwa"
        # comando = comando + f" -Dsonar.sources=app/DVWA -Dsonar.host.url={sonar_host} -Dsonar.token={sonar_dvwa_token}"
        # comando = comando + f" -Dsonar.login=mmpinto -Dsonar.password=@dm1n'"
        #comando = "sonar-scanner -X -Dsonar.projectKey={aplicacao} -Dsonar.sources=app/{aplicacao} -Dsonar.host.url={app_host} -Dsonar.token={app_token} -Dsonar.login={user} -Dsonar.password={password}"
        comando = "docker exec mn.sonar_cli bash -c '" + processar.sist_varredura_comando + "'" 
        #comando = processar.sist_varredura_comando 
        comando = comando.replace(comando, '{aplicacao}', processar.aplicacao_sigla)
        comando = comando.replace(comando, '{app_host}', processar.sist_varredura_ip_acesso)
        comando = comando.replace(comando, '{app_token}', processar.sist_varredura_token)
        comando = comando.replace(comando, '{user}', processar.sist_varredura_usuario)  
        comando = comando.replace(comando, '{password}', processar.sist_varredura_senha)  
        print (f"Comando: {comando}")
        try:
            stdin,stdout,stderr = ssh.exec_command(comando)
            stdin.write("docker\n")
            stdin.flush()    
            stdin.close()
            if stderr.readlines() != "[]":
                logger.error (stderr.readlines())
            else:
                logger.info (stdout.readlines())
        except paramiko.SSHException as e:
            print(f"Erro ao executar o comando remoto: {e}")
            logger.error (f"Erro ao executar o comando remoto: {e}")
        #3º passo: carregar o resultado da varredura
        if not processar.sist_varredura_webhook:  #se usar webhook o carregamento é feito pela chamado do webhook
            #comando = "docker exec mn.owasp_dc cat /src/report/dependency-check-report.json"
            comando = "docker exec mn.sonar_cli cat " + processar.caminho_resultado
            comando = comando.replace(comando, '{aplicacao}', processar.aplicacao_sigla)  
            print(comando)
            try:
                stdin,stdout,stderr = ssh.exec_command(comando)
                stdin.write("docker\n")
                stdin.flush()    
                stdin.close()
                # testar se retornou erro
                if stderr.channel.recv_exit_status() == 0:
                    print("Análise realizada com sucesso!")
                    data = json.dumps(stdout.readlines())
                    dados = json.loads(data.replace("\\','").replace("[\"','").replace("\"]','"))
                    print ("------------------------------------")
                    payload = json.dumps(dados,indent=3)
                    headers = {'Content-Type': 'application/json'}
                    response = requests.post('http://192.168.0.22:8000/api/v1/resultados/',data=payload, headers=headers)
                    if response.status_code == 201:
                        print("Dados inseridos no BD!")
                        logger.info (f"Resultado da análise {processar.aplicacao_sigla}-{processar.sist_varredura_sigla_tipo}.{processar.varredura} inserida no BD.")
                    else:
                        print("Erro ao enviar os dados para gravação no BD:", response.status_code)
                        logger.error (f"Erro ao salvar os dados no BD: {response.text}")
            except paramiko.SSHException as e:
                print(f"Erro ao executar o comando remoto: {e}")
                logger.error (f"Erro ao executar o comando remoto: {e}")
        ###########################    
        
    except ssh.SSHException as e:
        print(f"Erro ao conectar ao servidor remoto: {e}")
        logger.error (f"Erro ao conectar ao servidor remoto: {e}")
        return None
            
        
        
        
# # método para buscar os tipos de varredura da aplicação
# def get_sistemas_varredura(aplicacao_id):
#     """
#     Retorna os sistemas de varredura habilitados para a aplicação passada como parâmetro
#     """
#     # obtem a aplicação
#     aplicacao = requests.get(f'{url_base}/{aplicacao_id}') #, headers=headears)
#     if aplicacao.status_code == 200:
#         # obtem os sistemas de varredura habilitados para a aplicação
#         sistemas_varredura = aplicacao.json().get('sistemas_varredura')
#         return (sistemas_varredura)
#     else:
#         return (aplicacao.status_code)
    
# # métodos para processar a varredura do SonarQube
# def sonarQube_scan(ferramenta_url, aplicacao):
#     """
#     Conecta ao Sonar-CLI e inicia a varredura da aplicação

#     Args:
#         ferramenta_url (_type_): _description_
#         aplicacao (_type_): _description_
        
#     """
#     #headers = {'Authorization':'Token f0ee4a32f947f00cc06202ee306b5524fe1f3590'}
#     headers = {''}
#     url_login = f"{ferramenta_url}/api/authentication/login"
#     url_projetos = f"{ferramenta_url}/api/projects/search"

#     login = {
#         "login": "admin",
#         "password": "@dm1n"
#     }
#     # efetiva o o login no sonarQube
#     resultado = requests.post(url_login, headers=headers, data=login)  
#     # validar se autenticou corretamente
#     print(resultado.status_code)
#     #assert resultado.status_code == 201
    
#     # Conectar ao SonarQube via CLI /api/authentication/login
#     projeto = requests.get(url_projetos, headers=headers, data=f"projects=[{aplicacao}]")
#     print(projeto.json())
    
#     #sonar_cli =   docker.from_env()
#     return(None)
    
    

#    # Iniciar a varredura
#    #project_key = sonarQube_client.create_project(application_url, application_name)
#    #sonarQube_client.analyze_project(project_key, code_source_url)

#    # Obter os resultados da varredura
#    #results = sonarQube_client.get_issues(project_key)
#    #return results

# #método para processar a varredura do Owasp dependency-check
# def owaspDC_scan(ferramenta_url, aplicacao):
#     """_summary_

#     Args:
#         ferramenta_url (_type_): _description_
#         aplicacao (_type_): _description_

#     Returns:
#         _type_: _description_
#     """
#     return (None)

# # método para iniciar e obter os resultados da varredura para o OWASP ZAP
# def owaspZap_scan(ferramenta_url, aplicacao):
#     """Conecta ao owasp-zap e inicia a varredura da aplicação

#     Args:
#         ferramenta_url (_type_): _description_
#         aplicacao (_type_): _description_
#     """
#     # Iniciar o OWASP ZAP
# #    zap = owaspZap.Zap()
# #    zap.start()

#     # Adicionar a URL da aplicação à lista de alvos
# #    zap.spider(application_url)

#     # Executar a varredura
#     return (None)

# # método para obter a aplicação pelo nome
# def get_aplicacao(nome):
#     """
#     get_aplicacao - Retorna os dados da aplicação com a sigla passada como parâmetro

#     Args:
#         nome (string): sigla da aplicação a ser buscada
    
#     returns:
#         dict: dados da aplicação
#     """
#     try:
#         aplicacao = Aplicacao.objects.get(sigla=nome)
#         return aplicacao
#     except Aplicacao.DoesNotExist:
#         return None
    
#     # aplicacoes = requests.get(f"{url_base}/aplicacoes") #, headers=headears)
#     # if aplicacoes.status_code == 200:
#     #     for aplicacao in aplicacoes.json()['results']:
#     #         if aplicacao['sigla'] == nome:
#     #             return aplicacao
#     # return None


