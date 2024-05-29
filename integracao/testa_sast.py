import requests, seguranca.sast_scanner
# fixando para acesso com autenticação via token de umm usuário específico
headers = {'Authorization':'Token f0ee4a32f947f00cc06202ee306b5524fe1f3590'}


url_base_aplicacoes = 'http://localhost:8000/api/v2/aplicacoes/'
url_base_versoes = 'http://localhost:8000/api/v2/versoes/'


nova_aplicacao = {
   "nome": "Aplicação 3",
   "descricao": "Descrição da aplicação 3",
   "tipo": "1"
   
}

resultado = requests.post(url_base_aplicacoes, headers=headers, data=nova_aplicacao)  
#print(resultado.status_code)
assert resultado.status_code == 201


versoes = requests.get('http://locahost:8000/api/v2/versoes/', headers=headers)

print(versoes.json())  