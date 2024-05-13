import requests 


class TestVersoes:
   headears = {'Authorization':'Token f0ee4a32f947f00cc06202ee306b5524fe1f3590'}
   url_base_versoes = 'http://localhost:8000/api/v2/versoes/'
    
   def test_get_versoes(self):
      versao = requests.get(url=self.url_base_versoes, headers=self.headears)
      assert versao.status_code == 200
      assert versao.json()['count'] == 2
   
   def test_get_versao(self):
      versao = requests.get(url=f'{self.url_base_versoes}1/', headers=self.headears)
      assert versao.status_code == 200
      assert versao.json()['numero'] == '1.0.0'
      
   def test_post_versao(self):
      nova_versao = {
         "numero": "1.0.1",
         "descricao": "Descrição da versão 1.0.1",
         "aplicacao": "1"
      }
      resultado = requests.post(url=self.url_base_versoes, headers=self.headears, data=nova_versao)  
      assert resultado.status_code == 201
      assert resultado.json()['numero'] == nova_versao['numero']
      
   def test_put_versao(self):
      versao_atualizada = {
         "numero": "1.1.1",
         "descricao": "Descrição da versão 1.1.1",
         "aplicacao": "1"     
      }
      versao = requests.get(url=f'{self.url_base_versoes}1/', headers=self.headears)
      resultado = requests.put(url=f'{self.url_base_versoes}1/', headers=self.headears, data=versao_atualizada)  
      assert resultado.status_code == 200
      assert resultado.json()['numero'] == versao_atualizada ['numero']
      
   def test_delete_versao(self):
      resultado = requests.delete(url=f'{self.url_base_versoes}1/', headers=self.headears) 
      assert resultado.status_code == 204
      assert resultado.json() == None  
      
      
   