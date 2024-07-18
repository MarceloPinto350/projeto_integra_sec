import requests, json 

#url = 'http://192.168.0.13:32768/api/project_analyses/search?project=dvwa'
url = 'http://192.168.0.13:32768/api/project_analyses/search'
meuToken = 'squ_8e2c4df166d3f1e628ef57b8d0e373364552e84c'

sessao = requests.Session()
sessao.auth = meuToken, ''

chamada = getattr(sessao, 'get')

result = chamada(url)
print(result.status_code)

result_bin = result.content
retorno = json.loads(result_bin)
print(retorno)


