import requests

# GET Tipos de Aplicações

tiposaplicacooes = requests.get('http://locahost:8000/api/v2/tiposaplicacao/')
print (tiposaplicacooes.status_code)

# GET versões de aplicações
# para acesso com autenticação via token
headers = {'Authorization':'Token f0ee4a32f947f00cc06202ee306b5524fe1f3590'}
versoes = requests.get('http://locahost:8000/api/v2/versoes/', headers=headers)

print(versoes.json())  