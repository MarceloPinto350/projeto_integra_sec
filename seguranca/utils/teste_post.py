#import varredura

from ..models import Aplicacao #, SistemaVarredura,VersaoAplicacao,TipoVarredura

#headears = {'Authorization':'Token f0ee4a32f947f00cc06202ee306b5524fe1f3590'}
headears = {'Content-Type': 'application/json'}
url_base_aplicacoes = 'http://192.168.0.22:8000/varrer'
url_base_versoes = 'http://localhost:8000/varrer'


json =  { 
    "nome_aplicacao": "deposito-web", 
    "origem_processamento": "APP", 
    "sistema_varredura": ["SAST"] 
}

print(json['nome_aplicacao'])

apps = Aplicacao.objects.get(json['nome_aplicacao'])

print (apps)

#resultado = varredura.inicializa(json)
#print (resultado)
#resultado = requests.post(url_base_aplicacoes, headers=headears, data=json)  
#print(resultado.status_code)
#assert resultado.status_code == 201
