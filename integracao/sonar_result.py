import requests, json
headears = {'Authorization':'Token 61a384f801cb080e0c8f975c7731443b51c9f02e'}

url_base_aplicacoes = 'http://192.168.0.22:8000/api/v2/aplicacoes/'

# novo_resultado = {
#   "serverUrl": "http://localhost:9000",
#   "taskId": "AZA6b1EhB6xNrvqjPff-",
#   "status": "SUCCESS",
#   "analysedAt": "2024-06-21T10:54:39+0000",
#   "changedAt": "2024-06-21T10:54:39+0000",
#   "project": {
#     "key": "dvwa",
#     "name": "Damn Vulnerable Web Application",
#     "url": "http://localhost:9000/dashboard?id=dvwa"
#   },
#   "branch": {
#     "name": "main",
#     "type": "BRANCH",
#     "isMain": "true",
#     "url": "http://localhost:9000/dashboard?id=dvwa"
#   },
#   "qualityGate": {
#     "name": "Sonar way",
#     "status": "OK",
#     "conditions": [
#       {
#         "metric": "new_reliability_rating",
#         "operator": "GREATER_THAN",
#         "value": "1",
#         "status": "OK",
#         "errorThreshold": "1"
#       },
#       {
#         "metric": "new_security_rating",
#         "operator": "GREATER_THAN",
#         "value": "1",
#         "status": "OK",
#         "errorThreshold": "1"
#       },
#       {
#         "metric": "new_maintainability_rating",
#         "operator": "GREATER_THAN",
#         "value": "1",
#         "status": "OK",
#         "errorThreshold": "1"
#       },
#       {
#         "metric": "new_coverage",
#         "operator": "LESS_THAN",
#         "value": "0.0",
#         "status": "OK",
#         "errorThreshold": "80"
#       },
#       {
#         "metric": "new_duplicated_lines_density",
#         "operator": "GREATER_THAN",
#         "value": "0.0",
#         "status": "OK",
#         "errorThreshold": "3"
#       },
#       {
#         "metric": "new_security_hotspots_reviewed",
#         "operator": "LESS_THAN",
#         "status": "NO_VALUE",
#         "errorThreshold": "100"
#       }
#     ]
#   },
#   "properties": {
#     "sonar.analysis.detectedscm": "undetected",
#     "sonar.analysis.detectedci": "undetected"
#   }
# }

<<<<<<< HEAD
def processa_resultado(novo_resultado):
  try:
    data_execucao = novo_resultado['analysedAt']
    aplicacao = novo_resultado['project']['key'] 
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
=======
>>>>>>> 6acba307edf35a65b2dde3a7eab7f8f77f2f9041

    string_resultado={
      "aplicacao": versao_id,
      "resultado": novo_resultado,
      "data_resultado": data_execucao
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
