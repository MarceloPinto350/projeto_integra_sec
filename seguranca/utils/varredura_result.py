import requests, json
headears = {'Authorization':'Token 61a384f801cb080e0c8f975c7731443b51c9f02e'}

url_base_aplicacoes = 'http://192.168.0.22:8000/api/v2/aplicacoes/'

def get_sistema_varredura(resultado):
  retorno=''
  if "Sonar way" in resultado['qualityGate']['name']:
    retorno = "SonarQube"
  elif "Checkmarx" in resultado['qualityGate']['name']:
    retorno = "Checkmarx"
  #elif "OWASP Dependency Check" in resultado['reportSchema']['name']:
  elif "dependencies" in resultado.keys():
    retorno = "Owasp dependency-check"
  else:
    retorno = "Ferramenta não identificada"
  return (retorno)


def fetch_all_pages(base_url):
    """
    Função para buscar todas as páginas de resultados de uma API.

    Args:
        base_url (str): URL base da API.

    Yields:
        dict: Dicionário com os dados de cada página.
    """
    next_page = base_url
    while next_page:
        response = requests.get(next_page)
        response.raise_for_status ()  # Raise exception no caso de erro HTTP
        data = response.json()
        yield data
        next_page = data.get('next')  
    
  
def processa_resultado(novo_resultado,aplicacao="dvwa"):
  """
  Função para processar o resultado de uma varredura de segurança, identificando a versão da aplicação, ferramenta de análise, 
  data da varredura e a versão da aplicação à qual o resultado pertence.

  Args:
      novo_resultado (JSON): Resultado da varredura a ser processado
      aplicacao (str, optional): É a aplicação que está sendo avaliada. Default "dvwa".

  Returns:
      JSON: Restorna o resultado da varredura no padrão da AppSeg
  """
  try:
    estrutura = novo_resultado.keys()
    #print(estrutura)
    #print('---')
    ferramenta = ''
    aplicacao = ''
    data_execucao = ''
    #dados = json.dumps(novo_resultado)
    #print ("scanInfo" in estrutura)
    #print(f"Aplicação: {novo_resultado['projectInfo']['name']}")
    #print(f"Data: {novo_resultado['projectInfo']['reportDate']}")
    #print('---')
    
    if "qualityGate" in estrutura:
      ferramenta='SonarQube'
      data_execucao = novo_resultado['analysedAt']
      aplicacao = novo_resultado['project']['key']  
    elif "scanInfo" in estrutura:
      #if novo_resultado['scaninfo']['datasource'] == 'NVD API Last Modified':
      #print('---')
      ferramenta='Owasp dependency-check'
      data_execucao = novo_resultado['projectInfo']['reportDate']
      aplicacao = novo_resultado['projectInfo']['name']
    #data_execucao = novo_resultado['analysedAt'] if ferramenta == 'SonarQube' else novo_resultado['projectInfo']['reportDate']
    #aplicacao = novo_resultado['project']['key'] if aplicacao == None
    #print(aplicacao)
    #print(data_execucao)
    apps = requests.get(url_base_aplicacoes) #, headers=headears)
    versao_id = ""
    aplicacao_id = ""
    #print  (apps.status_code)
    if apps.status_code == 200:
      for app in apps.json().get('results'):
        if app['sigla'] == aplicacao.upper():
          aplicacao_id = app['id']
          #print(aplicacao_id)
          #versoes = requests.get(f'{url_base_aplicacoes}{aplicacao_id}/versoes')  #, headers=headears)
          #print ("====================")
          versoes = fetch_all_pages(f'{url_base_aplicacoes}{aplicacao_id}/versoes')
          for dados in versoes:
            #print(json.dumps(dados.get('results')[0]))
            #versao = json.dumps(dados.get('results')[0])
            versao = dados.get('results')[0]
            if ferramenta == 'SonarQube':
              print(f"Versão: {versao.get('nome_versao')} ==> {novo_resultado['branch']['name']}")
              if versao.get('nome_versao') == novo_resultado['branch']['name']:
                versao_id = versao.get('id')
            elif ferramenta == 'Owasp dependency-check':
              print(f"Versão: {versao.get('nome_versao')} ==> {versao.get('id')}")
              versao_id = versao.get('id')
          #print ("====================")
          #if versoes.status_code == 200:
          #  print(versoes.json())
          #  for versao in versoes.json().get('results'):
          #    print(f"Versão: {versao['nome_versao']} ==> {novo_resultado['branch']['name']}")
          #    if versao['nome_versao'] == novo_resultado['branch']['name']:
          #      versao_id = versao['id']
          #      break
          #else:
          #  return(versoes.status_code)
          break
    else:
      return(apps.status_code)  
    # obtem o sistema de varredura que gerou o resultado
    #sistemas_varredura = get_sistema_varredura(novo_resultado)
    sistemas_varredura = ferramenta
    # monta o resultado para ser armazenamento
    string_resultado={
      "aplicacao": versao_id,
      "resultado": novo_resultado,
      "data_resultado": data_execucao,
      "sistema_varredura": sistemas_varredura
      }

    #json_data = json.dumps(string_resultado)
    #return (json_data)
    return (string_resultado)
  except Exception as e:
    return (f'Erro ao processar o resultado: {e}')
  
#resultado = requests.post(url_base_resultado, headers=headears, data=novo_resultado)  
#print(resultado.status_code)
#assert resultado.status_code == 201
#
#aplicacao: Aplicação à qual o resultado pertence.
#resultado: Resultado da varredura de segurança.
#data_resultado: Data do resultado da varredura.
#sistema_varredura: Sistema de varredura que gerou o resultado.


# dados = {
#     "reportSchema": "1.1",
#     "scanInfo": {
#         "engineVersion": "9.2.0",
#         "dataSource": [
#             {
#                 "name": "NVD API Last Checked",
#                 "timestamp": "2024-06-25T03:35:23Z"
#             },
#             {
#                 "name": "NVD API Last Modified",
#                 "timestamp": "2024-06-25T03:15:10Z"
#             }
#         ]
#     },
#     "projectInfo": {
#         "name": "DVWA",
#         "reportDate": "2024-07-15T03:54:37.568238980Z",
#         "credits": {
#             "NVD": "This product uses the NVD API but is not endorsed or certified by the NVD. This report contains data retrieved from the National Vulnerability Database: https://nvd.nist.gov",
#             "CISA": "This report may contain data retrieved from the CISA Known Exploited Vulnerability Catalog: https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
#             "NPM": "This report may contain data retrieved from the Github Advisory Database (via NPM Audit API): https://github.com/advisories/",
#             "RETIREJS": "This report may contain data retrieved from the RetireJS community: https://retirejs.github.io/retire.js/",
#             "OSSINDEX": "This report may contain data retrieved from the Sonatype OSS Index: https://ossindex.sonatype.org"
#         }
#     },
#     "dependencies": [
#         {
#             "isVirtual": False,
#             "fileName": "add_event_listeners.js",
#             "filePath": "/src/DVWA/dvwa/js/add_event_listeners.js",
#             "md5": "957b8886269aa7eead6c411f91a60ce1",
#             "sha1": "c6b2c579fa0e2cca397e259177e0d863f0034507",
#             "sha256": "07d557fafc8d3c2b7fb0f3819cc967e9748631f0c66921a3d6a5115d2acb899f",
#             "evidenceCollected": {
#                 "vendorEvidence": [],
#                 "productEvidence": [],
#                 "versionEvidence": []
#             }
#         },
#         {
#             "isVirtual": False,
#             "fileName": "authbypass.js",
#             "filePath": "/src/DVWA/vulnerabilities/authbypass/authbypass.js",
#             "md5": "500454c8a8c8494aed049fa4330849e5",
#             "sha1": "dfbb7099071ad5de20429ea2a7bb72903fc87fcb",
#             "sha256": "4e5a493f5688bd8dff72e260742ad74a9cdb51e4a00bd223acf531094ffeb578",
#             "evidenceCollected": {
#                 "vendorEvidence": [],
#                 "productEvidence": [],
#                 "versionEvidence": []
#             }
#         },
#         {
#             "isVirtual": False,
#             "fileName": "dvwaPage.js",
#             "filePath": "/src/DVWA/dvwa/js/dvwaPage.js",
#             "md5": "2546c7f62818a204b5db73304482b10f",
#             "sha1": "7923fdd83cb8cf190ce75633ae03b1e368843fb7",
#             "sha256": "8f63a3712c245e146886cccaa2667a9da95192b853f568ddbdd76ebc67471e2d",
#             "evidenceCollected": {
#                 "vendorEvidence": [],
#                 "productEvidence": [],
#                 "versionEvidence": []
#             }
#         },
#         {
#             "isVirtual": False,
#             "fileName": "high.js",
#             "filePath": "/src/DVWA/vulnerabilities/csp/source/high.js",
#             "md5": "505c0ab7c850b3bb0e7382b641cf67b2",
#             "sha1": "9df5af3394d8bf06346fc0bae18aa731b09b5bbd",
#             "sha256": "74b8ad93bd24bf134ee8ec85f3f452a749d0f5880c968acb971d524f0bb7c850",
#             "evidenceCollected": {
#                 "vendorEvidence": [],
#                 "productEvidence": [],
#                 "versionEvidence": []
#             }
#         },
#         {
#             "isVirtual": False,
#             "fileName": "high.js",
#             "filePath": "/src/DVWA/vulnerabilities/javascript/source/high.js",
#             "md5": "b2fd53413a71f0fef5b557d113207163",
#             "sha1": "535fb4587fe024e0ad97e5a59384d93c9f46318a",
#             "sha256": "d5056bba3dc9a842c4a2b385c7e6a4e7bc64e2acf850f60db8dfcd1784ef0164",
#             "evidenceCollected": {
#                 "vendorEvidence": [],
#                 "productEvidence": [],
#                 "versionEvidence": []
#             }
#         },
#         {
#             "isVirtual": False,
#             "fileName": "high_unobfuscated.js",
#             "filePath": "/src/DVWA/vulnerabilities/javascript/source/high_unobfuscated.js",
#             "md5": "d80f63cbc54b786dd8f41515ceb42c4e",
#             "sha1": "7728c3c518569dd0029074b367094fc4cf49f354",
#             "sha256": "0f9a4c4a7ace15bde8f79d208d1d7c79cf554fc7da2ac7f82a31029ae3f261c0",
#             "evidenceCollected": {
#                 "vendorEvidence": [],
#                 "productEvidence": [],
#                 "versionEvidence": []
#             }
#         },
#         {
#             "isVirtual": False,
#             "fileName": "impossible.js",
#             "filePath": "/src/DVWA/vulnerabilities/csp/source/impossible.js",
#             "md5": "66fc1da1576785be1df90b1c09bbe09e",
#             "sha1": "6d14d847d0aeb3c4b29a37d76008b697597ceed2",
#             "sha256": "7d722f08d6651180147474405e1e6c32a933844df283626f37acb2e6e4ef1627",
#             "evidenceCollected": {
#                 "vendorEvidence": [],
#                 "productEvidence": [],
#                 "versionEvidence": []
#             }
#         },
#         {
#             "isVirtual": False,
#             "fileName": "medium.js",
#             "filePath": "/src/DVWA/vulnerabilities/javascript/source/medium.js",
#             "md5": "20c115b61344b11979b3e7593411ec7e",
#             "sha1": "a094a0943955dd271ce301f201d40f121fdc1d52",
#             "sha256": "6dab92dddb8516f532ac948964c2cd01bda494056a19e22550628e9870bebacb",
#             "evidenceCollected": {
#                 "vendorEvidence": [],
#                 "productEvidence": [],
#                 "versionEvidence": []
#             }
#         }
#     ]
# }

# print (processa_resultado(dados))
