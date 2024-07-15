# imports for models do Django
from django.db import models
from django.contrib.auth.models import User, Group

#imports diversos 
#from datetime import datetime, timedelta, date

# criação de uma classe abstrata para os modelos
class Base(models.Model):
   """
   Classe abstrata que define os atributos comuns a todos os modelos.
   Atributos:
      criacao: Data de criação do registro.
      modificacao: Data da última modificação do registro.
      ativo: Indica se o registro está ativo.
   """
   criacao = models.DateTimeField(auto_now_add=True)
   atualizacao = models.DateTimeField(auto_now=True)
   ativo = models.BooleanField(default=True)
   class Meta:
      abstract = True

# definição de valores constantes
SITUACAO_SW_CHOICES = (
   ['EM DESENVOLVIMENTO','Em desenvolvimento'],
   ['EM HOMOLOGAÇÃO', 'Em homologação'],
   ['EM IMPLANTAÇÃO','Em implantação'], 
   ['IMPLANTADO', 'Implantado'],
   ['DESCONTINUADO', 'Descontinuado'],
)
HOSPEDAGEM_CHOICES = (
   ['LOCAL', 'Local'],
   ['CLOUD', 'Cloud'],
   ['HÍBRIDO', 'Híbrido'],
   ['EXTERNO','Externo'],
)
CATEGORIA_CHOICES = (
   ['ADMINISTRATIVA','Administrativa'],
   ['TI','Tecnologia da Informação'], 
   ['JUDICIAL', 'Judicial'],  
)
ARQUITETURA_CHOICES = (
   ['WEB', 'Web'],
   ['CLIENTE/SERVIDOR','Cliente/Servidor'],
   ['MAINFRAME', 'Mainframe'],
)
ABRANGENCIA_CHOICES = (
   ['REGIONAL', 'Regional'],
   ['NACIONAL', 'Nacional'],
   ['CNJ','CNJ'],
)

SITUACAO_ATIVO_CHOICES = (
   ['ATIVO','Ativo'], 
   ['INATIVO','Desativado'], 
   ['EM MANUTENÇÃO','Em manutenção'],
   ['EM FALHA','Em falha'],
   ['DESCONTINUADO','Descontinuado'],
)
TIPO_REDE_CHOICES = (
   ['LAN','Local Area Network'],
   ['WAN','Wide Area Network'],
   ['WIFI','Rede sem fio'],
   ['VPN','Rede Privada Virtual'],
   ['DMZ','Zona Desmilitarizada'],
   ['INTRANET','Intranet'],
   ['EXTRANET','Extranet'],
)
TIPO_SERVIDOR_CHOICES = (
   ['ARQUIVOS','Servidor de arquivos'],
   ['WEB','Servidor Web'],
   ['BANCO_DADOS','Servidor de Banco de Dados'],
   ['APLICACAO','Servidor de Aplicação'],
   ['CORREIO','Servidor de Correio'],
   ['DNS','Servidor de DNS'],
   ['PROXY','Servidor Proxy'],
   ['FIREWALL','Servidor Firewall'],
   ['MONITORAMENTO','Servidor de Monitoramento'],
   ['BACKUP','Servidor de Backup'],
   ['LOGS','Servidor de Logs'],
   ['FTP','Servidor FTP'],
   ['MIDIA','Servidor de Mídia'],
   ['CLUSTER','Cluster'],
   ['OUTRO','Outros'],
)
TIPO_BANCO_DADOS_CHOICES = (
   ['ORACLE','Oracle'],
   ['SQLSERVER','SQL Server'],
   ['MYSQL','MySQL'],
   ['POSTGRESQL','PostgreSQL'],
   ['MONGODB','MongoDB'],
   ['COUCHDB','CouchDB'],
   ['REDIS','Redis'],
   ['NEO4J','Neo4j'],
   ['CASSANDRA','Cassandra'],
   ['MARIADB','MariaDB'],
   ['FIREBIRD','Firebird'],
   ['DB2','DB2'],
   ['SYBASE','Sybase'],
   ['INFORMIX','Informix'],
   ['SQLITE','SQLite'],
   ['H2','H2'],
   ['HSQLDB','HSQLDB'],
   ['DERBY','Derby'],
   ['OUTRO','Outro'],
)
   

# definição das classes
# Tipo de aplicação
class TipoAplicacao(models.Model):
   """ 
   Descreve os possíveis tipos de aplicação, 
   Pode ser classificados em: sistema, módulo, serviço, satélite, API, segurança etc. 
   Atributos: 
      nome: nome do tipo de aplicação
      descrição: descrição suscinta do tipo de aplicação
   """
   nome = models.CharField("Nome",max_length=100, unique=True, null=False)
   descricao = models.TextField("Descrição", max_length=1000)
   # define o nome padrão da tabela a ser criada no BD
   class Meta:
      db_table = "tb_tipo_aplicacao"
      verbose_name = 'Tipo de aplicação'
      verbose_name_plural = 'Tipos de aplicação'
      permissions = [
         ("can_view_tipo_aplicacao", "Can view tipos aplicação"),
         ("can_change_tipo_aplicacao", "Can change tipos aplicação"),
         ("can_add_tipo_aplicacao", "Can add tipos aplicação"),
         ("can_delete_tipo_aplicacao", "Can delete tipos aplicação"),
         ]
      ordering = ['nome']
   def __str__(self):
      return self.nome
   
# Área negocial
class AreaNegocial(models.Model):
   nome = models.CharField("Nome",max_length=200, unique=True,null=False)
   sigla = models.CharField("Sigla",max_length=20, unique=True, null=False)
   id_sigep = models.CharField("Código SIGEP",max_length=5, unique=True, null=False)
   ativa = models.BooleanField("Ativa",default=True,null=False)
   # define o nome padrão da tabela a ser criada no BD
   class Meta:
      db_table = "tb_area_negocial"
      verbose_name = 'Área Negocial'
      verbose_name_plural = 'Áreas Negociais'
      permissions = [
         ("can_view_area_negocial", "Can view areas negociais"),
         ("can_change_area_negocial", "Can change areas negociais"),
         ("can_add_area_negocial", "Can add areas negociais"),
         ("can_delete_area_negocial", "Can delete areas negociais"),
         ]
      ordering = ['nome']
   def __str__(self):
      return self.nome

# Aplicação
class Aplicacao(models.Model):
   """
   Define a classe Aplicação, que representa as aplicações de software a ser utilizado.
   Atributos:
      nome: nome da aplicação
      sigla: sigla da aplicação
      descricao: descrição suscinta dos objetivos e funcionamento da aplicação 
      categoria: categoria da aplicação
      abrangencia: abrangência da aplicação
      url_fonte: URL do código fonte da aplicação (GIT)
      area_responsavel: área responsável pela aplicação
      gestor_negocial: usuário que é indicado pelo gestor da área responsável como responsável pela aplicação
      data_registro: data de registro da aplicação
      data_atualizacao: data de atualização da aplicação
      data_descontinuacao: data que a aplicação foi descontinuada
      essencial: se a aplicação é essencial
      estrategico: se a aplicação é estratégica
      area_analista_liberacao: área da TI do analista de liberação
      arquitetura: arquitetura da aplicação
      tipo: tipo da aplicação
      hospedagem: tipo de hospedagem da aplicação
      url_acesso: URL de acesso à aplicação
      aplicacao_pai: aplicação pai, conforme o caso
      usuario_servico: usuário de serviço da aplicação
      senha_servico: senha do usuário de serviço da aplicação
      token_acesso: token de acesso à aplicação, conforme o caso
   """
   nome = models.CharField("Nome",max_length=255, unique=True,null=False)
   sigla = models.CharField("Sigla",max_length=20, unique=True)
   descricao = models.TextField("Descrição",max_length=1000)
   categoria = models.TextField("Categoria",default="ADMINISTRATIVA",null=False,choices=CATEGORIA_CHOICES)
   #abrangencia = models.TextField("Abrangência",default="REGIONAL",null=False,choices=ABRANGENCIA_CHOICES)   
   url_fonte = models.URLField("URL Fonte",unique=True,max_length=500,null=False)
   area_responsavel = models.ForeignKey(AreaNegocial, verbose_name="Área responsável",on_delete=models.CASCADE,null=False)
   #gestor_negocial = models.ForeignKey(User, verbose_name="Gestor responsável",on_delete=models.CASCADE)
   data_registro = models.DateTimeField("Data cadastro", auto_now_add=True, null=False)
   data_atualizacao = models.DateTimeField(auto_now=True)
   data_descontinuacao = models.DateField("Data descontinuação",null=True, blank=True)  
   #essencial = models.BooleanField("Essencial",default=True,null=False)
   #estrategico = models.BooleanField("Estratégico",default=False,null=False)
   #area_analista_liberacao = models.ForeignKey(AreaNegocial, verbose_name="Área analista liberação",on_delete=models.CASCADE)
   arquitetura = models.CharField("Arquitetura",max_length=20,default="WEB",null=False,choices=ARQUITETURA_CHOICES)
   tipo = models.ForeignKey(TipoAplicacao,on_delete=models.CASCADE,null=False)
   hospedagem = models.CharField("Hospedagem",max_length=20,default="LOCAL",null=False,choices=HOSPEDAGEM_CHOICES)
   url_acesso = models.URLField("URL Acesso",unique=True,max_length=500, null=False)                               
   aplicacao_pai = models.ForeignKey('self', verbose_name="Aplicação pai",on_delete=models.CASCADE,null=True, blank=True)
   usuario_servico = models.CharField("Usuário de serviço",max_length=50)
   senha_servico = models.CharField("Senha de serviço",max_length=50)
   token_acesso = models.CharField("Token de acesso",max_length=1000, null=True,blank=True)   
   # configurações de infrastrutura
   bancos_dados = models.ManyToManyField('BancoDados', related_name='aplicacoes_banco_dados', blank=True)
   servidores = models.ManyToManyField('Servidor', related_name='aplicacoes_servidor', blank=True)
   servicos = models.ManyToManyField('Servico', related_name='aplicacoes_servico', blank=True)  
   
   def __str__(self):
      return self.nome     
   def get_modulos(self):
      """Retorna os módulos relacionados à aplicação."""
      if self.tipo == TipoAplicacao.objects.get(nome='sistema'):
         return Aplicacao.objects.filter(tipo=TipoAplicacao.objects.get(nome='módulo'), aplicacao_relacionada=self)
      else:
         return None
   def get_infraestrutura(self):
      """Retorna a infraestrutura relacionada à aplicação."""
      if self.tipo == TipoAplicacao.objects.get(nome='sistema'):
         aplicacao_infraestrutura = Aplicacao.objects.filter(tipo=TipoAplicacao.objects.get(nome='infraestrutura'), aplicacao_relacionada=self)
         return aplicacao_infraestrutura
      else:
         return None
   def get_seguranca(self):
      """Retorna a segurança relacionada à aplicação."""
      if self.tipo == TipoAplicacao.objects.get(nome='sistema') or self.tipo == TipoAplicacao.objects.get(nome='satélite'):
         aplicacao_seguranca = Aplicacao.objects.filter(tipo=TipoAplicacao.objects.get(nome='segurança'), aplicacao_relacionada=self)
         return aplicacao_seguranca
      else:
         return None
   def get_ultima_versao(self):
      """Retorna a última versão da aplicação."""
      return VersaoAplicacao.objects.filter(aplicacao=self).latest('data_lancamento')
   class Meta:
      db_table = "tb_aplicacao"
      verbose_name = 'Aplicação'
      verbose_name_plural = 'Aplicações'
      permissions = [
         ("can_view_aplicacao", "Can view aplicações"),
         ("can_change_aplicacao", "Can change aplicações"),
         ("can_add_aplicacao", "Can add aplicações"),
         ("can_delete_aplicacao", "Can delete aplicações"),
         ]
      ordering = ['nome']

# Versão do Sistema
class VersaoAplicacao(models.Model):
   """
   Define as versões das aplicações.
   Atributos:
      aplicacao: Aplicação à qual a versão pertence
      nome_versao: Nome ou número da versão
      data_lancamento: Data de lançamento da versão
      descricao: Descrição da versão
      situacao: Situação da versão  
   """
   aplicacao = models.ForeignKey(Aplicacao, related_name='versoes',on_delete=models.CASCADE, null=False)
   nome_versao = models.CharField("Versão",max_length=50)
   data_lancamento = models.DateField("Data lançamento",null=False)
   descricao = models.TextField("Descrição",max_length=1000,null=False)
   situacao = models.CharField("Situação",default="EM DESENVOLVIMENTO",max_length=20,null=False,choices=SITUACAO_SW_CHOICES)
   sistema_varreduras = models.ManyToManyField('SistemaVarredura', related_name='versoes', blank=True)   
   def __str__(self):
        return f"{self.aplicacao.nome} v{self.nome_versao}"
   class Meta:    
      db_table = "tb_versao_aplicacao"
      unique_together = ['aplicacao', 'nome_versao']
      verbose_name = 'Versão da Aplicação'
      verbose_name_plural = 'Versões da Aplicação'
      permissions = [
         ("can_view_versao_aplicacao", "Can view versões aplicação"),
         ("can_change_versao_aplicacao", "Can change versões aplicação"),
         ("can_add_versao_aplicacao", "Can add versões aplicação"),
         ("can_delete_versao_aplicacao", "Can delete versões aplicação"),
         ]
      ordering = ['aplicacao','nome_versao']

class ResultadoScan(models.Model):
   """
   Define o resultado da varredura de segurança.
   Atributos:
      aplicacao: Versão da aplicação à qual o resultado pertence.
      resultado: Resultado da varredura de segurança.
      data_resultado: Data do resultado da varredura.
      sistema_varredura: Indica de qual sistema de varredura o resultado foi obtido.
   """
   aplicacao = models.ForeignKey(VersaoAplicacao, verbose_name="Aplicação",on_delete=models.CASCADE, null=False)
   resultado = models.JSONField("Resultado",null=False)
   data_resultado = models.DateTimeField("Data da análise",auto_now=True,null=False)
   sistema_varredura =  models.CharField("Sistema de varrredura",max_length=50)
   class Meta:
      db_table = "tb_resultado_scan"
      verbose_name = 'Resultado da Varredura'
      verbose_name_plural = 'Resultados da Varredura'
      permissions = [
         ("can_view_resultado_scan", "Can view resultados scan"),
         ("can_change_resultado_scan", "Can change resultados scan"),
         ("can_add_resultado_scan", "Can add resultados scan"),
         ("can_delete_resultado_scan", "Can delete resultados scan"),
         ]
      ordering = ['aplicacao','-data_resultado']
      #para colocar a ordenação em ordem decrescente usar o sinal de menos antes do campo
   def __str__(self):
      return f"Resultado da varredura de {self.aplicacao.nome}"
   def get_ultimo_resultado(self):
      """Retorna o último resultado da varredura."""
      return ResultadoScan.objects.filter(aplicacao=self.aplicacao).latest('data_resultado')

class TipoVarredura(models.Model):
   """
   Define os tipos de varredura de segurança.
   Atributos:
      nome: Nome do tipo de varredura.
      descricao: Descrição do tipo de varredura.
   """
   nome = models.CharField("Nome",max_length=50, unique=True,null=False)
   descricao = models.TextField("Descrição",max_length=1000)
   #sistemas_varredura = models.ManyToManyField('SistemaVarredura', related_name='tipos_varredura', blank=True)
   class Meta:
      db_table = "tb_tipo_varredura"
      verbose_name = 'Tipo de Varredura'
      verbose_name_plural = 'Tipos de Varredura'
      permissions = [
         ("can_view_tipo_varredura", "Can view tipos varredura"),
         ("can_change_tipo_varredura", "Can change tipos varredura"),
         ("can_add_tipo_varredura", "Can add tipos varredura"),
         ("can_delete_tipo_varredura", "Can delete tipos varredura"),
         ]
      ordering = ['nome']
   def __str__(self):
      return self.nome

class SistemaVarredura(models.Model):
   """
   Define os sistemas de varredura de segurança.
   Atributos:
      nome: Nome do sistema de varredura.
      descricao: Descrição do sistema de varredura.
      url: URL do sistema de varredura.
      usuario: Usuário do sistema de varredura.
      senha: Senha do sistema de varredura.
      token: Token do sistema de varredura.
      status: Status do sistema de varredura.
      tipos_varreduras: Tipos de sistema de varredura relacionados ao sistema.
      aplicacoes: Aplicações relacionadas ao sistema de varredura.
   """
   nome = models.CharField("Nome",max_length=100, unique=True,null=False)
   descricao = models.TextField("Descrição",max_length=1000)
   #tipo = models.ForeignKey(TipoVarredura, verbose_name="Tipo de Varredura",on_delete=models.CASCADE,null=False)
   url = models.URLField("URL",max_length=200,null=False)
   usuario = models.CharField("Usuário",max_length=50,null=True,blank=True)
   senha = models.CharField("Senha",max_length=50,null=True,blank=True)
   token = models.CharField("Token",max_length=1000,null=True,blank=True)
   status = models.CharField("Situação",max_length=20,null=False,choices=SITUACAO_ATIVO_CHOICES,default='ATIVO') 
   tipos_varreduras = models.ManyToManyField(TipoVarredura, related_name='sistema_varredura', blank=True)
   aplicacoes = models.ManyToManyField(VersaoAplicacao, related_name='sistemas_varredura', blank=True)
   class Meta:   
      db_table = "tb_sistema_varredura"
      verbose_name = 'Sistema de Varredura'
      verbose_name_plural = 'Sistemas de Varredura'
      permissions = [
         ("can_view_sistema_varredura", "Can view sistemas varredura"),
         ("can_change_sistema_varredura", "Can change sistemas varredura"),
         ("can_add_sistema_varredura", "Can add sistemas varredura"),
         ("can_delete_sistema_varredura", "Can delete sistemas varredura"),
         ]
      ordering = ['nome']
   def __str__(self):
      return self.nome
   @classmethod
   def get_by_nome(cls,nome):
      """ 
      Recupera a instância da classe pelo nome do sistema de varredura.
      Argumento: 
         nome (str): nome do sistema de varredura.
      Retorna:
         Instância da classe SistemaVarredura ou None, caso não exista.
      """
      try:
         return cls.objects.get(nome=nome)
      except cls.DoesNotExist:
         return None


# Classes relacionadas aos ativos de infraestrutura
# Tipos de ativos de infraestrutura
class TipoAtivoInfraestrutura(models.Model):
   """
   Define os tipos de ativos de infraestrutura 
   São os ativos cadastrados inicialmente no sistema: servidor, cluster, switch, armazenamento, banco de dados etc.
   Atributos:
      nome: Nome do tipo de ativo de infraestrutura.
      descricao: Descrição do tipo de ativo de infraestrutura.
   """
   nome = models.CharField(max_length=50, unique=True,null=False)
   descricao = models.TextField(max_length=1000)
   class Meta:
      db_table = "tb_tipo_ativo_infraestrutura"
      verbose_name = 'Tipo de Ativo de Infraestrutura'
      verbose_name_plural = 'Tipos de Ativos de Infraestrutura'
      permissions = [
         ("can_view_tipo_ativo_infraestrutura", "Can view tipos ativos infraestrutura"),
         ("can_change_tipo_ativo_infraestrutura", "Can change tipos ativos infraestrutura"),
         ("can_add_tipo_ativo_infraestrutura", "Can add tipos ativos infraestrutura"),
         ("can_delete_tipo_ativo_infraestrutura", "Can delete tipos ativos infraestrutura"),
         ]
      ordering = ['nome']
   def __str__(self):
      return self.nome

# Ativos de infraestrutura
class AtivoInfraestrutura(models.Model):
   """
   Define o ativo de infraestrutura.
   Atributos:
      nome: Nome do ativo de infraestrutura.
      descricao: Descrição do ativo de infraestrutura.
      tipo: Tipo do ativo de infraestrutura
      url_localizacao: Endereço da localização do ativo.
      endereco_ip: Endereço IP do ativo.
      porta_acesso: Porta de acesso para conectar ao ativo.
      usuario_acesso: Usuário de acesso ao ativo.s
      senha_acesso: Senha de acesso ao ativo.
      token_acesso: Token de acesso ao ativo.
      status: Status do ativo.
   """
   nome = models.CharField("Nome",max_length=255,null=False, unique=True)
   descricao = models.TextField("Descrição",max_length=1000, null=False)
   tipo = models.ForeignKey(TipoAtivoInfraestrutura, verbose_name="Tipo de Ativo", on_delete=models.CASCADE, null=False)
   url_localizacao = models.URLField("URL localização do ativo",max_length=200)
   endereco_ip = models.GenericIPAddressField("Endereço IP",protocol="IPv4",null=False)
   porta_acesso = models.IntegerField("Porta",null=False)
   usuario_acesso = models.CharField("Usuário de serviço",max_length=50)
   senha_acesso = models.CharField("Senha do usuário de serviço",max_length=50)
   token_acesso = models.CharField("Token de acesso ao ativo",max_length=1000)
   status = models.CharField("Situação do ativo",max_length=20, null=False, choices=SITUACAO_ATIVO_CHOICES)
   class Meta:
      db_table = "tb_ativo_infraestrutura"
      verbose_name = 'Ativo de Infraestrutura'
      verbose_name_plural = 'Ativos de Infraestrutura'
      permissions = [
         ("can_view_ativo_infraestrutura", "Can view ativos infraestrutura"),
         ("can_change_ativo_infraestrutura", "Can change ativos infraestrutura"),
         ("can_add_ativo_infraestrutura", "Can add ativos infraestrutura"),
         ("can_delete_ativo_infraestrutura", "Can delete ativos infraestrutura"),
         ]
      ordering = ['tipo','nome']
   def __str__(self):
      return self.nome

# Serviços de infraestrutura   
class Servico(models.Model):
   """
   Define os serviços de infraestrutura.
   Atributos:
      nome: Nome do serviço.
      descricao: Descrição do serviço.
      protocolo: Protocolo do serviço.
      url: URL do serviço.
      usuario: Usuário de acesso ao serviço.
      senha: Senha de acesso ao serviço.
      servidor: Servidor ao qual o serviço está hospedado.
      status: Status do serviço.
      data_cadastro: Data de cadastro do serviço.
      data_modificacao: Data de modificação do serviço.
      aplicacoes: Aplicações que utilizam o serviço.
   """
   nome = models.CharField("Nome",max_length=50, unique=True,null=False)
   descricao = models.TextField("Descrição",max_length=500,null=False)
   protocolo = models.CharField("Protocolo de serviço",max_length=50,null=False)
   url = models.URLField("URL",max_length=200)
   usuario = models.CharField("Usuário",max_length=50)
   senha = models.CharField("Senha",max_length=50)
   servidor = models.ForeignKey('Servidor', verbose_name="Servidor",on_delete=models.CASCADE,null=False) 
   status = models.CharField("Situação",max_length=20,null=False,choices=SITUACAO_ATIVO_CHOICES, default='ATIVO')
   data_cadastro = models.DateTimeField("Data Cadastro",auto_now_add=True,null=False)  
   data_modificacao = models.DateTimeField("Data Modificação",auto_now=True,null=False) 
   aplicacoes = models.ManyToManyField('Aplicacao', related_name='servico_aplicacoes', blank=True)  
   class Meta:
      db_table = "tb_servico"
      verbose_name = 'Serviço'
      verbose_name_plural = 'Serviços'
      permissions = [
         ("can_view_servico", "Can view serviços"),
         ("can_change_servico", "Can change serviços"),
         ("can_add_servico", "Can add serviços"),
         ("can_delete_servico", "Can delete serviços"),
         ]
      ordering = ['nome']
   def __str__(self):
      return self.nome      

# Servidores de infraestrutura   
class Servidor(models.Model):
   """
   Define os servidores de infraestrutura.
   Atributos:
      nome: Nome do servidor.
      descricao: Descrição do servidor.
      tipo: Tipo do servidor.
      ip: Endereço IP do servidor.
      sistema_operacional: Sistema operacional do servidor.
      arquitetura: Arquitetura do servidor.
      processador: Processador do servidor.
      memoria: Memória do servidor.
      disco: Disco do servidor.
      status: Status do servidor.
      data_cadastro: Data de cadastro do servidor.
      data_modificacao: Data de modificação do servidor.
      #rede: Rede à qual o servidor está conectado.
      servicos: Serviços hospedados no servidor.
      aplicacoes: Aplicações hospedadas no servidor.
   """
   nome = models.CharField("Nome",max_length=50, unique=True,null=False)
   descricao = models.TextField("Descrição",max_length=500)
   tipo = models.CharField("Tipo de servidor",max_length=50,choices=TIPO_SERVIDOR_CHOICES,null=False)
   ip = models.GenericIPAddressField("Endereço IP",protocol="IPv4",null=False)
   sistema_operacional = models.CharField("Sistema Operacional",max_length=50,null=False)
   arquitetura = models.CharField("Arquitetura",max_length=50,null=False)
   processador = models.CharField("Processador",max_length=50,null=False)
   memoria = models.CharField("Memória",max_length=50,null=False)
   disco = models.CharField("Disco",max_length=50,null=False)
   status = models.CharField("Situação",max_length=20,null=False,choices=SITUACAO_ATIVO_CHOICES,default='ATIVO')
   data_cadastro = models.DateTimeField("Data Cadastro",auto_now_add=True,null=False)  
   data_modificacao = models.DateTimeField("Data Modificação",auto_now=True,null=False)   
   #redes = models.ManyToManyRel(Rede, related_name='servidor_redes', blank=True)
   #rede = models.ForeignKey(Rede, verbose_name="Rede",on_delete=models.CASCADE,null=False)   
   servicos = models.ManyToManyField(Servico, related_name='servidor_servicos', blank=True)
   aplicacoes = models.ManyToManyField(Aplicacao, related_name='servidor_aplicacoes', blank=True)
   class Meta:
      db_table = "tb_servidor"
      verbose_name = 'Servidor'
      verbose_name_plural = 'Servidores'
      permissions = [
         ("can_view_servidor", "Can view servidores"),
         ("can_change_servidor", "Can change servidores"),
         ("can_add_servidor", "Can add servidores"),
         ("can_delete_servidor", "Can delete servidores"),
         ]
      ordering = ['nome']
   def __str__(self):
      return self.nome
   def get_redes(self):
      """Retorna as redes às quais o servidor está conectado."""
      return "\n".join([r.nome for r in Rede.objects.filter(servidores=self)])

# Redes de infraestrutura      
class Rede(models.Model):  
   """
   Define as redes de infraestrutura.
   Atributos:
      nome: Nome da rede.
      descricao: Descrição da rede.
      tipo: Tipo da rede.
      ip: Endereço IP da rede.
      mascara: Máscara de subrede da rede.
      gateway: Endereço IP do gateway da rede.
      dns_primario: Endereço IP do servidor DNS primário.
      dns_secundario: Endereço IP do servidor DNS secundário.
      status: Status da rede.
      data_cadastro: Data de cadastro da rede.
      data_modificacao: Data de modificação da rede.
      servidores: Servidores conectados à rede.
   """
   nome = models.CharField("Nome",max_length=50, unique=True,null=False)
   descricao = models.TextField("Descrição",max_length=500)
   tipo = models.CharField("Tipo de rede",max_length=50,choices=TIPO_REDE_CHOICES,default='LAN',null=False)
   ip = models.GenericIPAddressField("Endereço IP",protocol="IPv4",null=False)
   mascara = models.GenericIPAddressField("Máscara de subrede",protocol="IPv4",null=False)
   gateway = models.GenericIPAddressField("Gateway",protocol="IPv4",null=False)
   dns_primario = models.GenericIPAddressField("DNS Primário",protocol="IPv4",null=False)
   dns_secundario = models.GenericIPAddressField("DNS Secundário",protocol="IPv4",null=True,blank=True)
   status = models.CharField("Situação",max_length=20,null=False,choices=SITUACAO_ATIVO_CHOICES,default='ATIVO')
   data_cadastro = models.DateTimeField("Data Cadastro",auto_now_add=True,null=False) 
   data_modificacao = models.DateTimeField("Data Modificação",auto_now=True,null=False)   
   servidores = models.ManyToManyField(Servidor, related_name='rede_servidores', blank=True)  
   class Meta:
      db_table = "tb_rede"
      verbose_name = 'Rede'
      verbose_name_plural = 'Redes'
      permissions = [
         ("can_view_rede", "Can view redes"),
         ("can_change_rede", "Can change redes"),
         ("can_add_rede", "Can add redes"),
         ("can_delete_rede", "Can delete redes"),
         ]
      ordering = ['nome']
   def __str__(self):
      return self.nome 

# Bases de dados de infraestrutura   
class BancoDados(models.Model):
   """
   Define os bancos de dados de infraestrutura.
   Atributos:
      nome: Nome do banco de dados.
      descricao: Descrição do banco de dados.
      tipo: Tipo do banco de dados.
      ip: Endereço IP do banco de dados.
      porta: Porta de acesso ao banco de dados.
      usuario: Usuário de acesso ao banco de dados.
      senha: Senha de acesso ao banco de dados.
      status: Status do banco de dados.
      data_cadastro: Data de cadastro do banco de dados.
      data_modificacao: Data de modificação do banco de dados.
      servidor: Servidor ao qual o banco de dados está hospedado.
      aplicacoes: Aplicações relacionadas ao banco de dados.
   """
   nome = models.CharField("Nome",max_length=50, unique=True,null=False)
   descricao = models.TextField("Descrição",max_length=500, null=False)
   tipo = models.CharField("Tipo de banco de dados",max_length=50,choices=TIPO_BANCO_DADOS_CHOICES,null=False)
   ip = models.GenericIPAddressField("Endereço IP",protocol="IPv4",null=False)
   porta = models.IntegerField("Porta",null=False)
   usuario = models.CharField("Usuário",max_length=50,null=False)
   senha = models.CharField("Senha",max_length=50,null=False)
   status = models.CharField("Situação",max_length=20,null=False,choices=SITUACAO_ATIVO_CHOICES,default='ATIVO')
   data_cadastro = models.DateTimeField("Data Cadastro",auto_now_add=True,null=False)  
   data_modificacao = models.DateTimeField("Data Modificação",auto_now=True,null=False)   
   servidor = models.ForeignKey(Servidor, verbose_name="Servidor",on_delete=models.CASCADE,null=False)   
   aplicacoes = models.ManyToManyField(Aplicacao, related_name='bancodados_aplicacoes', blank=True)
   class Meta:
      db_table = "tb_banco_dados"
      verbose_name = 'Banco de Dados'
      verbose_name_plural = 'Bancos de Dados'
      permissions = [
         ("can_view_banco_dados", "Can view bancos dados"),
         ("can_change_banco_dados", "Can change bancos dados"),
         ("can_add_banco_dados", "Can add bancos dados"),
         ("can_delete_banco_dados", "Can delete bancos dados"),
         ]
      ordering = ['nome']
   def __str__(self):
      return self.nome
   

# Classes relacionadas aos documentos
class TipoModeloDocumento(models.Model):
   """
   Define os tipos de modelos de documentos.
   Atributos:
      nome: Nome do tipo de modelo de documento.
      descricao: Descrição do tipo de modelo de documento.
   """
   nome = models.CharField("Nome",max_length=10, unique=True,null=False)
   descricao = models.TextField("Descrição",max_length=1000)
   class Meta:
      db_table = "tb_tipo_modelo_documento"
      verbose_name = 'Tipo de Modelo de Documento'
      verbose_name_plural = 'Tipos de Modelo de Documento'
      permissions = [
         ("can_view_tipo_modelo_documento", "Can view tipos modelo documento"),
         ("can_change_tipo_modelo_documento", "Can change tipos modelo documento"),
         ("can_add_tipo_modelo_documento", "Can add tipos modelo documento"),
         ("can_delete_tipo_modelo_documento", "Can delete tipos modelo documento"),
         ]
      ordering = ['nome']
   def __str__(self):
      return self.nome
   
class ModeloDocumento(models.Model):
   """
   Define os modelos de documentos.
   Atributos:
      nome: Nome do modelo de documento.
      descricao: Descrição do modelo de documento.
      tipo: Tipo do modelo de documento.
      arquivo: Arquivo do modelo de documento.
      data_cadastro: Data de registro do modelo de documento.
      data_modificacao: Data de modificação do modelo de documento.
      ativa: Indica se o modelo de documento está ativo.
   """
   nome = models.CharField("Nome",max_length=100, unique=True,null=False)
   descricao = models.TextField("Descrição",max_length=1000)
   tipo = models.ForeignKey(TipoModeloDocumento, verbose_name="Tipo de Modelo",on_delete=models.CASCADE,null=False)
   arquivo = models.FileField("Arquivo",upload_to='documentos/',null=False)   
   data_cadastro = models.DateTimeField("Data Cadastro",auto_now_add=True,null=False)
   data_modificacao = models.DateTimeField("Data Modificação",auto_now=True,null=False)
   ativa = models.BooleanField("Ativa",default=True,null=False)
   
   class Meta:
      db_table = "tb_modelo_documento"
      verbose_name = 'Modelo de Documento'
      verbose_name_plural = 'Modelos de Documento'
      permissions = [
         ("can_view_modelo_documento", "Can view modelos documento"),
         ("can_change_modelo_documento", "Can change modelos documento"),
         ("can_add_modelo_documento", "Can add modelos documento"),
         ("can_delete_modelo_documento", "Can delete modelos documento"),
         ]
      ordering = ['nome']
   def __str__(self):
      return self.nome  