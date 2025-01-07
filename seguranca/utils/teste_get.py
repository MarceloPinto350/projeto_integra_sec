import requests

from seguranca.models import Aplicacao,VersaoAplicacao

headears = {'Authorization':'Token f0ee4a32f947f00cc06202ee306b5524fe1f3590'}

url_base_aplicacoes = 'http://localhost:8000/api/v2/aplicacoes/'
url_base_versoes = 'http://localhost:8000/api/v2/versoes/'

# GET Aplicações
# aplicacoes = requests.get(url_base_aplicacoes, headers=headears)
# print (aplicacoes.json())
# # testar se o status da requisição foi bem sucedido
# assert aplicacoes.status_code == 200

# # Testar a qantidade de resultados
# assert aplicacoes.json()['count'] == 2

app = Aplicacao.objects.get(sigla='DVWA')
print (app.nome, app.sigla, app.url_codigo_fonte)

versoes = VersaoAplicacao.objects.get(aplicacao=app.id)
for versao in versoes:
    print (versao.nome_versao, versao.url_codigo_fonte)