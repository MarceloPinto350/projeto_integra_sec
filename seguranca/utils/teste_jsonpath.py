import requests  
import jsonpath 

# GET Tipos de Aplicações
tiposaplicacooes = requests.get('http://192.168.0.9:8000/api/v2/tiposaplicacao/')
# mostrando o nome dos tipos de aplicação
resultados = jsonpath.jsonpath(tiposaplicacooes.json(),'results[*].nome')
print(resultados)


# GET Aplicações
