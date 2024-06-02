import docker.errors
import requests,docker,subprocess
import requests #, seguranca.sast_scanner
# fixando para acesso com autenticação via token de umm usuário específico
headers = {'Authorization':'Token f0ee4a32f947f00cc06202ee306b5524fe1f3590'}

url_base_aplicacoes = 'http://localhost:8000/api/v2/aplicacoes/'
url_base_versoes = 'http://localhost:8000/api/v2/versoes/'
url_base_sistemas_varredura = 'http://localhost:8000/api/v2/sistemasvarredura/'


nova_aplicacao = {
   "nome": "Aplicação 3",
   "descricao": "Descrição da aplicação 3",
   "tipo": "1"
   
}

#resultado = requests.post(url_base_aplicacoes, headers=headers, data=nova_aplicacao)  
#resultado = requests.post(url_base_aplicacoes, headers=headers, data=nova_aplicacao)  
#print(resultado.status_code)
##assert resultado.status_code == 201

# passos 
# 1º ) buscar as ferramentas de varredura que fazem SAST
# 2º ) buscar as versões da aplicação habilitadas para esse tipo de varredura
# 3º ) iniciar a varredura para cada versão da aplicação
# 4º ) obter os resultados da varredura
# 5º ) armazenar os resultados da varredura

tipo_varredura = 'SAST'
tipos_varredura = requests.get('http://locahost:8000/api/v2/tiposvarredura') #, headers=headers)  
print(tipos_varredura.json())

sistemas_varredura = requests.get(url_base_sistemas_varredura) #, headers=headers)
print(sistemas_varredura.json())  


#versoes = requests.get('http://locahost:8000/api/v2/versoes/', headers=headers)

#print(versoes.json())  