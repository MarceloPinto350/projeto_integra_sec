import requests

headears = {'Authorization':'Token f0ee4a32f947f00cc06202ee306b5524fe1f3590'}

url_base_aplicacoes = 'http://localhost:8000/api/v2/aplicacoes/'
url_base_versoes = 'http://localhost:8000/api/v2/versoes/'


versao_atualizada = {
   "numero": "1.1.1",
   "descricao": "Descrição da versão 1.1.1",
   "aplicacao": "1"     
}

versao = requests.get(url=f'url_base_versoes1/', headers=headears)
# print(versao.json())

resultado = requests.put(url=f'url_base_versoes1/', headers=headears, data=versao_atualizada)  
# testar se o status da requisição foi bem sucedido
assert resultado.status_code == 200

# testanto se a versão foi atualizada
assert resultado.json()['numero'] == versao_atualizada ['numero']