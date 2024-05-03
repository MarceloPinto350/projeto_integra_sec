# imports for models do Django
from django.db import models
from django.contrib.auth.models import User, Group

#imports diversos 
from datetime import datetime, timedelta, date

# definição de constantes
SITUACAO_SW_CHOICES = [
      ('EM DESENVOLVIMENTO', 'Em desenvolvimento'),
      ('EM HOMOLOGAÇÃO', 'Homologação'), 
      ('EM IMPLANTAÇÃO', 'Implantação'),
      ('IMPLANTADO', 'Implantado'),
      ('DESCONTINUADO', 'Descontinuado'),
   ]
TIPO_SW_CHOICES = ['SISTEMA', 'SATÉLITE', 'MÓDULO', 'INFRAESTRUTURA', 'INTERFACE',]

HOSPEDAGEM_CHOICES = ['LOCAL', 'CLOUD', 'HÍBRIDO', 'EXTERNO',]

ARQUITETURA_CHOICES = ['WEB', 'CLIENTE/SERVIDOR', 'MAINFRAME', ]

# definição das classes
# Categoria
class Categoria(models.Model):
   categoria = models.CharField("Categoria",max_length=100, unique=True,null=False)
   ativa = models.BooleanField("Ativa",default=True,null=False)
   def __str__(self):
        return self.nome

# Abrangência
class Abrangencia(models.Model):
   abrangencia = models.CharField("Abrangência",max_length=100, unique=True,null=False)
   ativa = models.BooleanField("Ativa",default=True,null=False)
   def __str__(self):
      return self.nome

# Área negocial
class AreaNegocial(models.Model):
   area_negocial = models.CharField("Área Negocial",max_length=200, unique=True,null=False)
   sigla = models.CharField("Sigla",max_length=20, unique=True, null=False)
   identificador_sigep = models.CharField("Código SIGEP",max_length=5, unique=True, null=False)
   ativa = models.BooleanField("Ativa",default=True,null=False)
   def __str__(self):
      return self.nome



# Sistema
class Sistema(models.Model):
      nome = models.CharField("Nome",max_length=255, unique=True,null=False)
      sigla = models.CharField("Sigla",max_length=20, unique=True)
      descricao = models.TextField("Descrição"max_length=1000)
      categoria = models.ForeignKey(Categoria,verbose_name="Categoria",on_delete=models.CASCADE,null=False)
      abrangencia = models.ForeignKey(Abrangencia,verbose_name="Abragência",default="Regional", null=False)   
      url_fonte = models.URLField("URL Fonte",max_length=500, null=False)
      area_responsavel = models.ForeignKey(AreaNegocial, verbose_name="Área responsável",on_delete=models.CASCADE,null=False)
      gestor_negocial = models.ForeignKey(User, verbose_name="Gestor responsável",on_delete=models.CASCADE)
      data_registro = models.DateTimeField("Data cadastro",auto_now=False, auto_now_add=True, null=False)
      data_atualizacao = models.DateTimeField(auto_now=True)
      data_descontinuacao = models.DateTimeField("Data descontinuação",null=True)
      essencial = models.BooleanField("Essencial",default=True,null=False)
      estrategico = models.BooleanField("Estratégico",default=False,null=False)
      area_analista_liberacao = models.ForeignKey(AreaNegocial, verbose_name="Área analista liberação",on_delete=models.CASCADE)
      arquitetura = models.CharField("Arquitetura",max_length=20,default="WEB",null=False,choices=ARQUITETURA_CHOICES)
      tipo_software = models.CharField("Tipo de software",max_length=20,default="SISTEMA",null=False,choices=TIPO_SW_CHOICES)
      hospedagem = models.CharField("Hospedagem",max_length=20,default="LOCAL",null=False,choices=HOSPEDAGEM_CHOICES)
      url_acesso = models.URLField("URL Acesso",max_length=500, null=False)                               
      def __str__(self):
         return self.nome  
   
# SistemaVersao
class SistemaVersao(models.Model):
   sistema = models.ForeignKey(Sistema,verbose_name="Sistema",on_delete=models.CASCADE,null=False)
   versao = models.CharField("Versão",max_length=20, unique=True,null=False)
   data_registro = models.DateTimeField(auto_now_add=True, null=False)
   data_atualizacao = models.DateTimeField(auto_now=True)
   situacao = models.CharField(default="EM DESENVOLVIMENTO",max_length=20,null=False,choices=SITUACAO_SW_CHOICES)
   def __str__(self):
      return self.versao
   
class SistemaConfiguracao(models.Model):
   sistema = models.ForeignKey(Sistema,verbose_name="Sistema",on_delete=models.CASCADE,null=False)
   versao = models.ForeignKey(SistemaVersao,verbose_name="Versão",on_delete=models.CASCADE,null=False)
   descricao = models.TextField("Descrição",max_length=1000)
   data_registro = models.DateTimeField(auto_now_add=True, null=False)
   data_atualizacao = models.DateTimeField(auto_now=True)
   def __str__(self):
      return self.descricao