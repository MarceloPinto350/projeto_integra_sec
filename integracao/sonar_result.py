import requests

headears = {'Authorization':'Token f0ee4a32f947f00cc06202ee306b5524fe1f3590'}

url_base_resultado = 'http://localhost:8000/api/v2/resultadosscan/'

def 

novo_resultado = {
   "aplicacao": "versão xpto"
   "resultado": "resultado JSON"
   "data_resultado": "datahora"   
}

resultado = requests.post(url_base_resultado, headers=headears, data=novo_resultado)  
#print(resultado.status_code)
assert resultado.status_code == 201
