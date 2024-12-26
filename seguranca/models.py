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
SITUACAO_VARREDURA_CHOICES = (
   ['EM ANDAMENTO', 'Em andamento'],
   ['CONCLUÍDA', 'Concluída'],
   ['FALHA', 'Falha'],
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
TIPO_AMBIENTE_CHOICES = (
   ['PRODUÇÃO','Produção'],
   ['HOMOLOGAÇÃO','Homologação'],
   ['DESENVOLVIMENTO','Desenvolvimento'],
   ['TESTE','Teste'],
   ['BUGFIX','Bugfix'],
   ['TREINAMENTO','Treinamento'],
   ['OUTRO','Outro'],
)
TIPO_ARQUIVO_CHOICES = (
   ['JSON','JSON'],
   ['YAML','YAML'],
   ['XML','XML'],
   ['CSV','CSV'],
   ['XLS','XLS'],
   ['XLSX','XLSX'],
   ['DOC','DOC'],
   ['DOCX','DOCX'],
   ['PDF','PDF'],
   ['TXT','TXT'],
   ['ODF','ODF'],
   ['ODS','ODS'],
   ['OUTRO','Outro'],
)
TIPO_MODELO_DOCUMENTO_CHOICES = (
   ['POD', 'POD'],
   ['SERVICES','Services'],
   ['INGRESS','Ingress'],
   ['CONFIGMAP','ConfigMap'],
   ['SECRET','Secret'],
   ['PERSISTENT_VOLUME','Persistent Volume'],
   ['PERSISTENT_VOLUME_CLAIM','Persistent Volume Claim'],
   ['STATEFUL_SET','Stateful Set'],
   ['DEPLOYMENT','Deployment'],
   ['JOB','Job'],
   ['CRONJOB','CronJob'],
   ['SERVICE_ACCOUNT','Service Account'],
   ['ROLE','Role'],
   ['ROLE_BINDING','Role Binding'],
   ['CLUSTER_ROLE','Cluster Role'],
   ['CLUSTER_ROLE_BINDING','Cluster Role Binding'],
   ['NETWORK_POLICY','Network Policy'],
   ['POD_SECURITY_POLICY','Pod Security Policy'],
   ['CUSTOM_RESOURCE_DEFINITION','Custom Resource Definition'],
   ['OUTRO','Outro'],
)

# Definição das classes propriamente ditas

# CLASSES BÁSICAS
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
   
# Tipo de varredura
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

# Tipo de relacionamento
class TipoRelacionamento(models.Model):
   """
   Define os tipos de relacionamento entre as aplicações e os componentes de infraestrutura
   Atributos:
      nome: Nome do relacionamento
      descricao: Descrição do relacionamento
   """
   nome = models.CharField("Nome",max_length=50, unique=True,null=False)
   descricao = models.TextField("Descrição",max_length=1000)
   class Meta:
      db_table = "tb_tipo_relacionamento"
      verbose_name = 'Tipo de Relacionamento'
      verbose_name_plural = 'Tipos de Relacionamento'
      permissions = [
         ("can_view_tipo_relacionamento", "Can view tipos relacionamento"),
         ("can_change_tipo_relacionamento", "Can change tipos relacionamento"),
         ("can_add_tipo_relacionamento", "Can add tipos relacionamento"),
         ("can_delete_tipo_relacionamento", "Can delete tipos relacionamento"),
         ]
      ordering = ['nome']
   
# Modelo de documento
class ModeloDocumento(models.Model):
   """
   Define os modelos de documentos.
   Atributos:
      nome: Nome do modelo de documento.
      descricao: Descrição do modelo de documento.
      tipo_modelo: Tipo do modelo de documento.
      data_cadastro: Data de registro do modelo de documento.
      data_modificacao: Data de modificação do modelo de documento.
      ativo: Indica se o modelo de documento está ativo.
      modelo: Modelo de documento propriamente dito.
   """
   nome = models.CharField("Nome",max_length=100, unique=True,null=False)
   descricao = models.TextField("Descrição",max_length=200, null=False)
   tipo_modelo = models.CharField("Tipo Modelo de Documento",max_length=50,null=False,choices=TIPO_MODELO_DOCUMENTO_CHOICES,default='OUTRO')
   data_cadastro = models.DateTimeField("Data Cadastro",auto_now_add=True,null=False)
   data_modificacao = models.DateTimeField("Data Modificação",auto_now=True,null=False)
   ativo = models.BooleanField("Ativo",default=True,null=False)
   modelo = models.TextField("Modelo",max_length=3000,null=False)   
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
   
# Aplicação
class Aplicacao(models.Model):
   """
   Define a classe Aplicação, que representa as aplicações de software a ser utilizado.
   Atributos:
      nome: nome da aplicação
      sigla: sigla da aplicação
      descricao: descrição suscinta dos objetivos e funcionamento da aplicação 
      categoria: categoria da aplicação
      arquitetura: arquitetura da aplicação
      abrangencia: abrangência da aplicação
      hospedagem: tipo de hospedagem da aplicação
      url_código_fonte: URL do código fonte da aplicação
      area_responsavel: área responsável pela aplicação
      #gestor_negocial: usuário que é indicado pelo gestor da área responsável como responsável pela aplicação
      tipo_aplicacao: tipo da aplicação
      essencial: se a aplicação é essencial
      estrategica: se a aplicação é estratégica
      #area_analista_liberacao: área da TI do analista de liberação
      usuario_servico: usuário de serviço da aplicação
      data_registro: data de registro da aplicação
      data_atualizacao: data de atualização da aplicação
      data_descontinuacao: data que a aplicação foi descontinuada
   """
   nome = models.CharField("Nome",max_length=255, unique=True,null=False)
   sigla = models.CharField("Sigla",max_length=20, unique=True)
   descricao = models.TextField("Descrição",max_length=1000)
   categoria = models.TextField("Categoria",default="ADMINISTRATIVA",null=False,choices=CATEGORIA_CHOICES)
   arquitetura = models.CharField("Arquitetura",max_length=20,default="WEB",null=False,choices=ARQUITETURA_CHOICES)
   abrangencia = models.TextField("Abrangência",default="REGIONAL",null=False,choices=ABRANGENCIA_CHOICES)   
   hospedagem = models.CharField("Hospedagem",max_length=20,default="LOCAL",null=False,choices=HOSPEDAGEM_CHOICES)
   url_codigo_fonte = models.URLField("URL Fonte",unique=True,max_length=500,null=False)
   area_responsavel = models.ForeignKey(AreaNegocial, verbose_name="Área responsável",on_delete=models.CASCADE,null=False)
   #gestor_negocial = models.ForeignKey(User, verbose_name="Gestor responsável",on_delete=models.CASCADE)
   #area_analista_liberacao = models.ForeignKey(AreaNegocial, verbose_name="Área analista liberação",on_delete=models.CASCADE,null=False)
   tipo_aplicacao = models.ForeignKey(TipoAplicacao,on_delete=models.CASCADE,null=False)
   aplicacao_pai = models.ForeignKey('self', verbose_name="Aplicação pai",on_delete=models.CASCADE,null=True, blank=True)
   essencial = models.BooleanField("Essencial",default=True,null=False)
   estrategica = models.BooleanField("Estratégica",default=False,null=False)
   usuario_servico = models.CharField("Usuário de serviço",max_length=50,default='servico',null=False)
   data_registro = models.DateTimeField("Data cadastro", auto_now_add=True, null=False)
   data_atualizacao = models.DateTimeField(auto_now=True)
   data_descontinuacao = models.DateField("Data descontinuação",null=True, blank=True)  
   
   def __str__(self):
      return self.nome     
   def get_modulos(self):
      """Retorna os módulos relacionados à aplicação."""
      if self.tipo == TipoAplicacao.objects.get(nome='sistema'):
         return Aplicacao.objects.filter(tipo=TipoAplicacao.objects.get(nome='módulo'), aplicacao_relacionada=self)
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

# Versão da aplicação
class VersaoAplicacao(models.Model):
   """
   Define as versões das aplicações.
   Atributos:
      aplicacao: Aplicação à qual a versão pertence
      nome_versao: Nome ou número da versão
      data_lancamento: Data de lançamento da versão
      descricao: Descrição da versão
      url_acesso: URL de acesso à aplicacao configurada
      senha_servico: Senha de acesso à aplicação
      token_acesso: Token de acesso à aplicação
      data_homologacao: Data de homologação da versão
      data_producao: Data de produção da versão
      situacao: Situação da versão  
   """
   aplicacao = models.ForeignKey(Aplicacao, related_name='versoes',on_delete=models.CASCADE, null=False)
   nome_versao = models.CharField("Versão",max_length=50)
   data_lancamento = models.DateField("Data lançamento",null=False)
   descricao = models.TextField("Descrição",max_length=1000,null=False)
   url_acesso = models.URLField("URL de acesso à aplicação",max_length=200,null=True,blank=True)
   senha_servico = models.CharField("Senha de serviço",max_length=50,null=True,blank=True)
   token_acesso = models.CharField("Token de acesso",max_length=1000,null=True,blank=True)
   data_homologacao = models.DateField("Data homologação",null=True, blank=True) 
   data_producao = models.DateField("Data produção",null=True, blank=True)
   situacao = models.CharField("Situação",default="EM DESENVOLVIMENTO",max_length=20,null=False,choices=SITUACAO_SW_CHOICES)
   def __str__(self):
        return f"{self.aplicacao.nome} v{self.nome_versao}"
   def get_versao_atual(self):
      """Retorna a versão atual da aplicação."""
      return VersaoAplicacao.objects.filter(aplicacao=self.aplicacao).latest('data_producao')
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

# Sistema de varredura
class SistemaVarredura(models.Model):
   """
   Define os sistemas de varredura de segurança.
   Atributos:
      aplicacao_seguranca: Aplicação de segurança à qual o sistema de varredura está relacionado.
      tipo_varredura: Tipo de varredura do sistema.
      usa_webhook: Indica se o sistema de varredura usa webhook.
      comando: Comando de varredura do sistema.
      ip_acesso: Endereço IP de acesso ao sistema de varredura.
      usuario: Usuário do sistema de varredura.
      senha: Senha do sistema de varredura.
      token: Token de acesso ao sistema de varredura.
      situacao: Situação do sistema de varredura.
      aplicacoes: A lista de aplicações que habilitadas para usar o sistema de varredura.
   """
   aplicacao_seguranca = models.ForeignKey(Aplicacao, verbose_name="Aplicação de Segurança",on_delete=models.CASCADE,null=False)
   tipo_varredura = models.ForeignKey(TipoVarredura, verbose_name="Tipo de Varredura",on_delete=models.CASCADE,null=False)
   usa_webhook = models.BooleanField("Usa Webhook",default=False,null=False)
   comando = models.CharField("Comando",max_length=1000, null=False)
   ip_acesso = models.GenericIPAddressField("Endereço IP",protocol="IPv4",null=False)
   usuario = models.CharField("Usuário",max_length=50,null=True,blank=True)
   senha = models.CharField("Senha",max_length=50,null=True,blank=True)
   token = models.CharField("Token",max_length=1000,null=True,blank=True)
   situacao = models.CharField("Situação",max_length=20,null=False,choices=SITUACAO_ATIVO_CHOICES,default='ATIVO')
   aplicacoes = models.ManyToManyField(VersaoAplicacao, related_name='aplicacoes_varridas', blank=True)
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
      ordering = ['aplicacao_seguranca','tipo_varredura']
   def get_aplicacoes(self):
      """Retorna a lista de aplicações habilitadas para usar o sistema de varredura."""
      return self.aplicacoes.all()
   def __str__(self):
      return self.aplicacao_seguranca.nome + ' - ' + self.tipo_varredura.nome

# Varreduras de vulnerabilidade
class Varredura(models.Model):
   """
   Define as varreduras de vulnerabilidade realizadas.

   Atributos:
      aplicacao: Aplicação à qual a varredura pertence.
      origem: Origem da varredura.
      data_inicio: Data de início da varredura.
      data_fim: Data de final da varredura.
      vulnerabilidades: Número de vulnerabilidades encontradas.
      erros: Número de erros encontrados.
      situacao: Situação da varredura.
      log: Log contendo os detalhes da execução da varredura.
   """
   aplicacao= models.ForeignKey(Aplicacao, verbose_name="Aplicação",on_delete=models.CASCADE,null=False)
   origem = models.CharField("Origem",max_length=100,null=False)
   data_inicio = models.DateTimeField("Data Início")
   data_fim = models.DateTimeField("Data Fim")
   vulnerabilidades = models.IntegerField("Vulnerabilidades",default=0,null=False)
   erros = models.IntegerField("Erros",default=0,null=False)
   situacao = models.CharField("Situação",max_length=20,null=False,choices=SITUACAO_VARREDURA_CHOICES)
   log = models.FileField("Log",upload_to='logs/',null=True,blank=True)
   class Meta:
      db_table = "tb_varredura"
      verbose_name = 'Varredura'
      verbose_name_plural = 'Varreduras'
      permissions = [
         ("can_view_varredura", "Can view varreduras"),
         ("can_change_varredura", "Can change varreduras"),
         ("can_add_varredura", "Can add varreduras"),
         ("can_delete_varredura", "Can delete varreduras"),
         ]
      ordering = ['aplicacao','-data_inicio']

# Resultado de varredura de vulnerabilidades
class ResultadoScan(models.Model):
   """
   Define o resultado da varredura de segurança.
   Atributos:
      aplicacao: Versão da aplicação à qual o resultado pertence.
      varredura: Varredura à qual o resultado pertence.
      sistema_varredura: Indica de qual sistema de varredura o resultado foi obtido.
      data_resultado: Data do resultado da varredura.
      resultado: Resultado da varredura de segurança.
   """
   aplicacao = models.ForeignKey(VersaoAplicacao, verbose_name="Aplicação",on_delete=models.CASCADE, null=False)
   varredura = models.ForeignKey(Varredura, verbose_name="Varredura",on_delete=models.CASCADE, null=False)
   sistema_varredura = models.ForeignKey(SistemaVarredura, verbose_name="Sistema de Varredura",on_delete=models.CASCADE, null=False)
   data_resultado = models.DateTimeField("Data da análise",auto_now=True,null=False)
   resultado = models.JSONField("Resultado",null=False)
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

# Ativos de infraestrutura
class AtivoInfraestrutura (models.Model):
   """
   Define a classe para os ativos de infraestrutura.
   Atributos:
      nome: Nome do ativo de infraestrutura.
      descricao: Descrição do ativo de infraestrutura.
      tipo_ativo: Tipo do ativo de infraestrutura
      data_cadastro: Data de registro do ativo de infraestrutura.
      data_modificacao: Data de modificação do ativo de infraestrutura.
      situacao: Indica a situação do ativo, conforme SITUACAO_ATIVO_CHOICES.
   """
   nome = models.CharField("Nome",max_length=255,null=False, unique=True)
   descricao = models.TextField("Descrição",max_length=1000, null=False)
   tipo_ativo = models.ForeignKey(TipoAtivoInfraestrutura, verbose_name="Tipo de Ativo", on_delete=models.CASCADE, null=False)
   data_cadastro = models.DateTimeField("Data Cadastro",auto_now_add=True,null=False)
   data_modificacao = models.DateTimeField("Data Modificação",auto_now=True,null=False)
   situacao = models.CharField("Situação do ativo",max_length=20, null=False, choices=SITUACAO_ATIVO_CHOICES)
   class Meta:
      #abstract = True
      db_table = "tb_ativo_infraestrutura"
      verbose_name = 'Ativo de Infraestrutura'
      verbose_name_plural = 'Ativos de Infraestrutura'
      permissions = [
         ("can_view_ativo_infraestrutura", "Can view ativos infraestrutura"),
         ("can_change_ativo_infraestrutura", "Can change ativos infraestrutura"),
         ("can_add_ativo_infraestrutura", "Can add ativos infraestrutura"),
         ("can_delete_ativo_infraestrutura", "Can delete ativos infraestrutura"),
         ]
      ordering = ['tipo_ativo','nome']
   def __str__(self):
      return self.nome
   
# Configuração da aplicação   
class Configuracao (models.Model):
   """
   Define a configuração da aplicação.
   Atributos:
      versao_aplicacao: Versão da aplicação relacionada
      ativo_infraestrutura: Ativo de infraestrutura relacionado 
      descricao: Descrição da configuração
      ambiente: Ambiente da configuração
      url_acesso: URL de acesso à aplicacao configurada
      senha_servico: Senha de acesso à aplicação
      token_acesso: Token de acesso à aplicação
   """
   versao_aplicacao = models.ForeignKey(VersaoAplicacao, related_name='configuracoes',on_delete=models.CASCADE, null=False)
   ativo_infraestrutura = models.ForeignKey(AtivoInfraestrutura, related_name='configuracoes',on_delete=models.CASCADE, null=False)
   descricao = models.TextField("Descrição",max_length=1000)
   ambiente = models.CharField("Ambiente",default="DESENVOLVIMENTO",max_length=50,null=False,choices=TIPO_AMBIENTE_CHOICES)
   class Meta:
      db_table = "tb_configuracao"
      verbose_name = 'Configuração'
      verbose_name_plural = 'Configurações'
      permissions = [
         ("can_view_configuracao", "Can view configurações"),
         ("can_change_configuracao", "Can change configurações"),
         ("can_add_configuracao", "Can add configurações"),
         ("can_delete_configuracao", "Can delete configurações"),
         ]
   def __str__(self):
      return f"{self.versao_aplicacao.aplicacao.nome} v{self.versao_aplicacao.nome_versao} - {self.ativo_infraestrutura.nome} ({self.ambiente})"
   
# Arquivo de configuração da aplicação
class ArquivoConfiguracao(models.Model):
   """
   Define os arquivos de configuração da aplicação.
   
   Atributos:
      configuracao: Configuração da aplicação à qual o arquivo de configuração pertence.
      descricao: Descrição do arquivo de configuração.
      modelo_documento: Modelo de documento utilizado como base para a criação do arquivo de configuração.
      tipo_arquivo: Tipo de arquivo de configuração.
      data_cadastro: Data de cadastro do arquivo de configuração.
      data_modificacao: Data de modificação do arquivo de configuração.
      arquivo: Conteúdo do arquivo de configuração propriamente dito.
   """
   configuracao= models.ForeignKey(Configuracao, verbose_name="Configuração",on_delete=models.CASCADE,null=False)
   descricao = models.TextField("Descrição",max_length=500,null=False)
   modelo_documento = models.ForeignKey(ModeloDocumento, verbose_name="Modelo de Documento",on_delete=models.CASCADE)
   tipo_arquivo = models.CharField("Tipo de Arquivo",default="JSON",max_length=20,null=False,choices=TIPO_ARQUIVO_CHOICES)
   data_cadastro = models.DateTimeField("Data Cadastro",auto_now_add=True,null=False)
   data_modificacao = models.DateTimeField("Data Modificação",auto_now=True,null=False)   
   arquivo= models.TextField("Arquivo",max_length=3000,null=False)
   def __str__(self):
      return f"{self.configuracao.versao_aplicacao.aplicacao.nome} v{self.configuracao.versao_aplicacao.nome_versao} - {self.descricao}"
   class Meta:
      db_table = "tb_arquivo_configuracao"
      verbose_name = 'Arquivo de Configuração'
      verbose_name_plural = 'Arquivos de Configuração'
      permissions = [
         ("can_view_arquivo_configuracao", "Can view arquivos configuração"),
         ("can_change_arquivo_configuracao", "Can change arquivos configuração"),
         ("can_add_arquivo_configuracao", "Can add arquivos configuração"),
         ("can_delete_arquivo_configuracao", "Can delete arquivos configuração"),
         ]
      ordering = ['configuracao','descricao']
   
# Relacionamento entre aplicações e ativos de infraestrutura
class Relacionamento (models.Model):
   """
   Define o relacionamento entre as aplicações e os Ativos de Infraestrutura
   Atributos:
      aplicacao: Aplicação relacionada
      ativo_infraestrutura: Ativo de infraestrutura relacionado
      tipo_relacao: Tipo do relacionamento
   """
   aplicacao = models.ForeignKey(Aplicacao, related_name='ativos_relacionados',on_delete=models.CASCADE, null=False)
   ativo_infraestrutura = models.ForeignKey(AtivoInfraestrutura, related_name='aplicacoes_relacionadas',on_delete=models.CASCADE, null=False)
   tipo_relacao = models.ForeignKey(TipoRelacionamento, verbose_name="Tipo de Relacionamento",on_delete=models.CASCADE,null=False)
   class Meta:
      db_table = "tb_relacionamento"
      verbose_name = 'Relacionamento'
      verbose_name_plural = 'Relacionamentos'
      permissions = [
         ("can_view_relacionamento", "Can view relacionamentos"),
         ("can_change_relacionamento", "Can change relacionamentos"),
         ("can_add_relacionamento", "Can add relacionamentos"),
         ("can_delete_relacionamento", "Can delete relacionamentos"),
         ]
   def __str__(self):
      return f"{self.aplicacao.nome} - {self.ativo_infraestrutura.nome} ({self.tipo_relacao})"

# Classes relacionadas aos ativos de infraestrutura e serviços
# Redes de infraestrutura      
class Rede(models.Model):  
   """
   Define as redes de infraestrutura.
   Atributos:
      tipo: Tipo da rede.
      ip: Endereço IP da rede.
      mascara: Máscara de subrede da rede.
      gateway: Endereço IP do gateway da rede.
      ativo_infraestrutura: Ativo de infraestrutura ao qual a rede está relacionada.
   """
   tipo = models.CharField("Tipo de rede",max_length=50,choices=TIPO_REDE_CHOICES,default='LAN',null=False)
   ip = models.GenericIPAddressField("Endereço IP",protocol="IPv4",null=False)
   mascara = models.GenericIPAddressField("Máscara de subrede",protocol="IPv4",null=False)
   gateway = models.GenericIPAddressField("Gateway",protocol="IPv4",null=False)
   ativo_infraestrutura = models.ForeignKey(AtivoInfraestrutura, verbose_name="Ativo de Infraestrutura",on_delete=models.CASCADE,null=False)
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
      ordering = ['tipo']
   def __str__(self):
      return (self.tipo, " - ", self.ip, " - ", self.mascara) 

# Serviço de infraestrutura   
class Servico(models.Model):
   """
   Define os serviços de infraestrutura.
   Atributos:
      nome_servico: Nome do serviço.
      protocolo: Protocolo do serviço.
      porta: Porta de acesso ao serviço.
      url: URL de acesso ao serviço.
      usuario: Usuário de acesso ao serviço.
      senha: Senha de acesso ao serviço.
      ativo_infraestrutura: Ativo de infraestrutura ao qual o serviço está relacionado.
   """
   nome_servico = models.CharField("Nome do serviço",max_length=50,null=False,unique=True)  
   protocolo = models.CharField("Protocolo de serviço",max_length=50,null=False)
   porta = models.IntegerField("Porta de serviço",null=False)
   url = models.URLField("URL",max_length=200)
   usuario = models.CharField("Usuário",max_length=50)
   senha = models.CharField("Senha",max_length=50)
   ativo_infraestrutura = models.ForeignKey(AtivoInfraestrutura, verbose_name="Ativo de Infraestrutura",on_delete=models.CASCADE,null=False)
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
      ordering = ['nome_servico']
   def __str__(self):
      return (self.nome_servico, " - ", self.url)

# Bases de dados de infraestrutura   
class BancoDados(models.Model):
   """
   Define os bancos de dados de infraestrutura.
   Atributos:
      nome: Nome do banco de dados.
      tipo: Tipo do banco de dados.
      ambiente: Ambiente do banco de dados.
      ativo_infraestrutura: Ativo de infraestrutura ao qual o banco de dados está relacionado.
      porta: Porta de acesso ao banco de dados.
      versao: versão do banco de dados.
      string_conexao: String de conexão para o banco de dados.
   """
   nome = models.CharField("Nome do banco de dados",max_length=100,null=False,unique=True)
   tipo = models.CharField("Tipo de banco de dados",max_length=50,choices=TIPO_BANCO_DADOS_CHOICES,null=False)
   ambiente = models.CharField("Ambiente",max_length=50,null=False,choices=TIPO_AMBIENTE_CHOICES,default='DESENVOLVIMENTO')
   ativo_infraestrutura = models.ForeignKey(AtivoInfraestrutura, verbose_name="Ativo de Infraestrutura",on_delete=models.CASCADE,null=True)
   porta = models.IntegerField("Porta",null=False, default=1521) 
   versao = models.TextField("Versão",max_length=50,null=True,default='1.0')
   string_conexao = models.TextField("String de Conexão",max_length=1000,null=False)
   
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
      ordering = ['tipo']
   def __str__(self):
      return (self.tipo, " - ", self.versao)

# Servidores de infraestrutura   
class Servidor(models.Model):
   """
   Define os servidores de infraestrutura.
   Atributos:
      tipo: Tipo do servidor.
      sistema_operacional: Sistema operacional do servidor.
      arquitetura: Arquitetura do servidor.
      processador: Processador do servidor.
      memoria: Memória do servidor.
      disco: Tamanho do espaço em disco do servidor.
      redes: Redes de infraestrutura associadas ao servidor.
      servicos: Serviços de infraestrutura associados ao servidor.
      bancos_dados: Bancos de dados de infraestrutura associados ao servidor.
   """
   tipo = models.CharField("Tipo de servidor",max_length=50,choices=TIPO_SERVIDOR_CHOICES,null=False)
   sistema_operacional = models.CharField("Sistema Operacional",max_length=50,null=False)
   arquitetura = models.CharField("Arquitetura",max_length=50,null=False)
   processador = models.CharField("Processador",max_length=50,null=False)
   memoria = models.CharField("Memória",max_length=50,null=False)
   disco = models.CharField("Disco",max_length=50,null=False)
   redes = models.ManyToManyField(Rede, related_name='servidores', blank=True)
   servicos = models.ManyToManyField(Servico, related_name='servidores', blank=True)
   bancos_dados = models.ManyToManyField(BancoDados, related_name='servidores', blank=True)
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
      ordering = ['tipo']
   def get_redes(self):
      """Retorna as redes associadas ao servidor."""
      return self.redes.all()
   def get_servicos(self):
      """Retorna os serviços associados ao servidor."""
      return self.servicos.all()
   def get_bancos_dados(self):
      """Retorna os bancos de dados associados ao servidor."""
      return self.bancos_dados.all()
   def __str__(self):
      return (self.tipo, " - ", self.sistema_operacional)

   