import requests, json, logging, datetime, paramiko
 
from ..models import Aplicacao, SistemaVarredura,VersaoAplicacao,TipoVarredura

url_base = 'http://127.0.0.1:8000/api/v2'
headers = {'Content-Type': 'application/json'}



logger = logging.getLogger(__name__)
    
# método que inicia a análise e processa a varredura da aplicação, conforme o caso
def inicializa(processar):
    """
    Inicializar as variáveis de ambiente
    Recebe os dados passados através de um JSON para processar a varredura da aplicação
    processar={
      "nome_aplicacao": "DVWA",
      "origem_processamento": "API",
      "sistema_varredura": ["ALL","SAST","DAST","SCA"]
      }
    Devolve a vaeeruda a ser cadsatrada no BD
    varredura = {
        "origem": origem,
        "data_inicio": dth_inicio,
        "data_fim": dth_termino,
        "situacao": 'EM ANDAMENTO', # FALHA|EM ANDAMENTO|CONCLUÍDA
        "aplicacao": apps.id,
        "log": None,
    }
    """
    print ("Inicializando a varredura...")
    logger.info("Inicializando a varredura...")
    try:
        nomeApp = processar['nome_aplicacao']
        origem = processar['origem_processamento']
        sistema = processar['sistema_varredura']
    except KeyError:
        msg = "Erro na estrtura do JSON encaminhado."
        logger.error (msg)
        print (msg)
        return ({"mensagem": msg})
    
    #registrando o inicio do processamento...
    dth_inicio = datetime.datetime.now()
    logger.info(f"Iniciando o processamento da varredura da aplicação {nomeApp}...")
    
    # buscar Dados da aplicação
    apps = Aplicacao.objects.get(sigla=nomeApp)
    logger.info(f"Aplicação a ser verificada: {apps.id}, {apps.nome}, {nomeApp}, {apps.url_codigo_fonte}")
    logger.info("Parâmetros de processamento: {processar}")
    #print (f"Aplicação a ser verificada: {apps.id}, {apps.nome}, {nomeApp}, {apps.url_codigo_fonte}")
    
    # buscar os tipos de varreduras habilitados para a aplicação
    #print (sistema)
    if  "ALL" in sistema:
        tipos_varredura = TipoVarredura.objects.all()
    else:    
        tipos_varredura = TipoVarredura.objects.filter(nome__in=sistema)
    #print (f"Tipos de varredura habilitados para aplicação: {tipos_varredura}")
    # buscar os sistemas de varredura habilitados para a aplicação
    sistemas_varredura = SistemaVarredura.objects.filter(situacao='ATIVO')
    lista_sistemas = []
    for sist_varr in sistemas_varredura:
        # pega a lista de versões da aplicação vinculadas ao sistema de varredura
        lista = sist_varr.aplicacoes.all()
        for appx in lista:
            # pega a aplicação da versão
            Vapp = VersaoAplicacao.objects.get(id=appx.id)
            if Vapp.aplicacao.id == apps.id:
                # adiciona a lista de sistemas de varredura habilitados para a aplicação
                lista_sistemas.append(sist_varr.aplicacao_seguranca.id)
    print (f"Lista de sistemas de varredura habilitados para aplicação: {lista_sistemas}")
    logger.info(f"Lista de sistemas de varredura habilitados para aplicação: {lista_sistemas}")
    
    # gera a configuração da varredura
    dth_termino = datetime.datetime.now()
    varredura = {
        "origem": origem,
        "data_inicio": dth_inicio,
        "data_fim": dth_termino,
        "situacao": 'EM ANDAMENTO', # FALHA|EM ANDAMENTO|CONCLUÍDA
        "aplicacao": apps.id,
        "log": None,
    }
    logger.info(f"Gravando a varredura para aplicação: {varredura}")    
    return (varredura)


        
        
        


