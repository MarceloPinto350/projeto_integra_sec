import requests

headears = {'Authorization':'Token f0ee4a32f947f00cc06202ee306b5524fe1f3590'}

url_base_aplicacoes = 'http://localhost:8000/api/v2/aplicacoes/'
url_base_versoes = 'http://localhost:8000/api/v2/versoes/'


resultado = requests.delete(url=f'{url_base_versoes}1/', headers=headears) 
# testar se o status da requisição foi bem sucedido
assert resultado.status_code == 204
# testar se a versão foi deletada
assert resultado.json() == None
