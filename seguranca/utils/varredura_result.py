import requests, json
headears = {'Authorization':'Token 61a384f801cb080e0c8f975c7731443b51c9f02e'}

url_base_aplicacoes = 'http://192.168.0.22:8000/api/v2/aplicacoes/'

def get_sistema_varredura(resultado):
  retorno=''
  if "Sonar way" in resultado['qualityGate']['name']:
    retorno = "SonarQube"
  elif "Checkmarx" in resultado['qualityGate']['name']:
    retorno = "Checkmarx"
  elif "Owasp dependency-check" in resultado['qualityGate']['name']:
    retorno = "Owasp dependency-check"
  else:
    retorno = "Outro"
  return (retorno)
  
def processa_resultado(novo_resultado,aplicacao="dvwa"):
  try:
    estrutura = novo_resultado.keys()
    ferramenta = ''
    if "qualityGate" in estrutura:
      ferramenta='SonarQube'
      data_execucao = novo_resultado['analysedAt']
      aplicacao = novo_resultado['project']['key']  
    elif "scaninfo" in estrutura:
      if novo_resultado['scaninfo']['datasource'] == 'NVD API Last Modified':
        ferramenta='Owasp dependency-check'
        data_execucao = novo_resultado['projectInfo']['reportDate']
        aplicacao = novo_resultado['projectInfo']['name']
    #data_execucao = novo_resultado['analysedAt'] if ferramenta == 'SonarQube' else novo_resultado['projectInfo']['reportDate']
    #aplicacao = novo_resultado['project']['key'] if aplicacao == None
    #print(aplicacao)
    #print(data_execucao)
    apps = requests.get(url_base_aplicacoes) #, headers=headears)
    if apps.status_code == 200:
      for app in apps.json().get('results'):
        if app['sigla'] == aplicacao.upper():
          aplicacao_id = app['id']
          print(aplicacao_id)
          versoes = requests.get(f'{url_base_aplicacoes}{aplicacao_id}/versoes')  #, headers=headears)
          if versoes.status_code == 200:
            #print(versoes.json())
            for versao in versoes.json().get('results'):
              if versao['nome_versao'] == novo_resultado['branch']['name']:
                versao_id = versao['id']
                break
          else:
            return(versoes.status_code)
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
