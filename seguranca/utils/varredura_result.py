import requests, logging, os 

from ..models import Varredura, SistemaVarredura, Aplicacao, VersaoAplicacao

headears = {'Authorization':'Token 61a384f801cb080e0c8f975c7731443b51c9f02e'}

logger = logging.getLogger(__name__)  

#url_base = "http://192.168.0.22:8000/api/"
#url_base_aplicacoes = f"{url_base}v2/aplicacoes/"
url_api = os.getenv('URL_API')
url_base_aplicacoes = f"{url_api}/v2/aplicacoes/"


def get_sistema_varredura(resultado):
  retorno=''
  if "Sonar way" in resultado['qualityGate']['name']:
    retorno = "SonarQube"
  elif "Checkmarx" in resultado['qualityGate']['name']:
    retorno = "Checkmarx"
  #elif "OWASP Dependency Check" in resultado['reportSchema']['name']:
  elif "dependencies" in resultado.keys():
    retorno = "Owasp dependency-check"
  else:
    retorno = "Ferramenta não identificada"
  return (retorno)


def fetch_all_pages(base_url):
    """
    Função para buscar todas as páginas de resultados de uma API.

    Args:
        base_url (str): URL base da API.

    Yields:
        dict: Dicionário com os dados de cada página.
    """
    next_page = base_url
    while next_page:
        response = requests.get(next_page)
        response.raise_for_status ()  # Raise exception no caso de erro HTTP
        data = response.json()
        yield data
        next_page = data.get('next')  
    
  
def processa_resultado(novo_resultado,aplicacao="dvwa"):
  """
  Função para processar o resultado de uma varredura de segurança, identificando a versão da aplicação, ferramenta de análise, 
  data da varredura e a versão da aplicação à qual o resultado pertence.

  Args:
      novo_resultado (JSON): Resultado da varredura a ser processado
      aplicacao (str, optional): É a aplicação que está sendo avaliada. Default "dvwa".

  Returns:
      JSON: Retorna o resultado da varredura no padrão da AppSeg
  """
  estrutura = novo_resultado.keys()
  ferramenta = ''
  aplicacao = ''
  data_execucao = ''
  #print(f"{estrutura}\n")
  #print(f"{url_base_aplicacoes}\n")
  
  if "qualityGate" in estrutura:
    ferramenta='SonarQube'
    data_execucao = novo_resultado['analysedAt']
    aplicacao = novo_resultado['project']['key']  
  elif "scanInfo" in estrutura:
    ferramenta='Owasp dependency-check'
    data_execucao = novo_resultado['projectInfo']['reportDate']
    aplicacao = novo_resultado['projectInfo']['name']
  # elif "status" in estrutura:
  #   resultado = novo_resultado['status']  
  #   ferramenta='SonarQube'
  #   data_execucao = novo_resultado['analysedAt']
  #   aplicacao = novo_resultado['project']['key']  

  print(ferramenta,data_execucao, aplicacao, str(aplicacao).upper())

  # obter os dados da aplicação
  try:
    #apps = requests.get(url_base_aplicacoes) #, headers=headears)
    app = Aplicacao.objects.get(sigla=str(aplicacao).upper())    #id=2)
    versao_id = ""
    aplicacao_id = app.id
    print(f"Aplicação: {aplicacao_id} - {app.nome} - {app.sigla}")
    # obter a última versão da aplicação em 
    try:
      #versoes = VersaoAplicacao.objects.filter(aplicacao=aplicacao_id,situacao='IMPLANTADO').order_by('-data_lancamento').first()
      #versoes = fetch_all_pages(f'{url_base_aplicacoes}{apps.id}/versoes')
      versao = VersaoAplicacao.objects.filter(aplicacao=aplicacao_id).order_by('-data_lancamento').first()
      print(f"Ferramenta: {ferramenta} - Versão: {versao.nome_versao} ==> {versao.id}")
      if ferramenta == 'SonarQube':
        if versao.nome_versao == novo_resultado['branch']['name']:
          versao_id = versao.id
      elif ferramenta == 'Owasp dependency-check':
        versao_id = versao.id
      # obtem o sistema de varredura que gerou o resultado
      #sistemas_varredura = get_sistema_varredura(novo_resultado)
      try:
        app_seg = Aplicacao.objects.get(nome=ferramenta)
        sistemas_varredura = SistemaVarredura.objects.get(aplicacao_seguranca=app_seg.id)
        # monta o resultado para ser armazenamento
        # busca a último varredura realziada ainda em aberto
        try:
          varredura = Varredura.objects.filter(aplicacao=aplicacao_id,situacao='EM ANDAMENTO').order_by('-data_inicio').first()
          print (f"Varredura: {varredura.id}")
          string_resultado={
            "data_resultado": data_execucao,
            "resultado": novo_resultado,
            "aplicacao": versao_id, 
            "varredura": varredura.id,
            "sistema_varredura": sistemas_varredura.id
            }
          #print(string_resultado)
          #json_data = json.dumps(string_resultado)
          #return (json_data)
          return (string_resultado)
        except Exception as e1:
          print(f"Não conseguiu localizar varredura em andamento para a ferramenta {ferramenta} na aplicação {app.sigla}: {e1}")
          return (f"Não conseguiu localizar varredura em andamento para a ferramenta {ferramenta} na aplicação {app.sigla}: {e1}")
      except Exception as e2:
        print (f"Não conseguiu localizar o sistema de varredura {ferramenta}: {e2}")
        return (f"Não conseguiu localizar o sistema de varredura {ferramenta}: {e2}")
    except Exception as e3:
      print(f"Não conseguiu localizar última versão da aplicação {aplicacao}: {e3}")
      return (f"Não conseguiu localizar última versão da aplicação {aplicacao}: {e3}")
  except Exception as e4:
    print (f'Não conseguiu localizar a aplicação {aplicacao}: {e4}')
    return (f'Não conseguiu localizar a aplicação {aplicacao}: {e4}')

    
  # try:
  #   #apps = requests.get(url_base_aplicacoes) #, headers=headears)
  #   app = Aplicacao.objects.get(sigla=aplicacao.upper)
  #   versao_id = ""
  #   aplicacao_id = app.id
  #   versao = ""
  #   print(f"Aplicação: {app.id} - {app.nome} - {app.sigla} ({app.status_code})")
  #   if apps.status_code == 200:
  #     versoes = fetch_all_pages(f'{url_base_aplicacoes}{apps.id}/versoes')
  #     for dados in versoes:
  #       versao = dados.get('results')[0]
  #       if ferramenta == 'SonarQube':
  #         #print(f"Ferramenta: {ferramenta} - Versão: {versao.get('nome_versao')} ==> {novo_resultado['branch']['name']}")
  #         if versao.get('nome_versao') == novo_resultado['branch']['name']:
  #           versao_id = versao.get('id')
  #       elif ferramenta == 'Owasp dependency-check':
  #         print(f"Ferramenta: {ferramenta} - Versão: {versao.get('nome_versao')} ==> {versao.get('id')}")
  #         versao_id = versao.get('id')
  #     # obtem o sistema de varredura que gerou o resultado
  #     #sistemas_varredura = get_sistema_varredura(novo_resultado)
  #     print(f"Ferramenta: {ferramenta} - Versão: {versao.get('nome_versao')} ==> {versao.get('id')}")
  #     try:
  #       app_seg = Aplicacao.objects.get(nome=ferramenta)
  #       sistemas_varredura = SistemaVarredura.objects.get(aplicacao_seguranca=app_seg.id)
  #       # monta o resultado para ser armazenamento
  #       # busca a último varredura realziada ainda em aberto
  #       varredura = Varredura.objects.filter(aplicacao=aplicacao_id,situacao='EM ANDAMENTO').order_by('-data_inicio').first()
  #       print (f"Varredura: {varredura.id}")
  #       string_resultado={
  #         "data_resultado": data_execucao,
  #         "resultado": novo_resultado,
  #         "aplicacao": versao_id, #aplicacao_id,
  #         "varredura": varredura.id,      
  #         "sistema_varredura": sistemas_varredura.id
  #         }
  #       print(string_resultado)
  #       #json_data = json.dumps(string_resultado)
  #       #return (json_data)
  #       return (string_resultado)
  #     except Exception as e1:
  #       print(f'Erro ao processar o resultado: {e1}')
  #       return (f'Erro ao processar o resultado: {e1}')
  #   else:
  #     print (f"Erro ao buscar dados da aplicação {aplicacao}: {apps.status_code}") 
  #     return (f"Erro ao buscar dados das aplicações {aplicacao}: {apps.status_code}")   
  #   except Exception as e2:
  #     print(f"Erro ao buscar dados das aplicações {aplicacao}: {e2}")
  #     return (f"Erro ao buscar dados das aplicações {aplicacao}: {e2}")
  # except Exception as e:
  #   print(f"Erro ao processar o resultado: {e}")
  #   return (f"Erro ao processar o resultado: {e}")
  
#resultado = requests.post(url_base_resultado, headers=headears, data=novo_resultado)  
#print(resultado.status_code)
#assert resultado.status_code == 201
#
#aplicacao: Aplicação à qual o resultado pertence.
#resultado: Resultado da varredura de segurança.
#data_resultado: Data do resultado da varredura.
#sistema_varredura: Sistema de varredura que gerou o resultado.

