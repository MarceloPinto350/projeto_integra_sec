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
TIPO_SW_CHOICES = ['SISTEMA', 'SATÉLITE', 'MÓDULO', 'OUTRO']

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
      url = models.URLField("URL",max_length=500)
      area_responsavel = models.ForeignKey(AreaNegocial, verbose_name="Área responsável",on_delete=models.CASCADE)
      gestor_negocial = models.ForeignKey(User, verbose_name="Gestor responsável",on_delete=models.CASCADE)
      data_registro = models.DateTimeField("Data cadastro",auto_now=False, auto_now_add=True, null=False)
      data_atualizacao = models.DateTimeField(auto_now=True)
      essencial = models.BooleanField("Essencial",default=True,null=False)
      area_analista_liberacao = models.ForeignKey(AreaNegocial, verbose_name="Área analista liberação",on_delete=models.CASCADE)
      arquitetura = models.CharField("Arquitetura",max_length=100)
      def __str__(self):
         return self.nome  
   
# SistemaVersao
class SistemaVersao(models.Model):
   sistema = models.ForeignKey(Sistema,verbose_name="Sistema",on_delete=models.CASCADE,null=False)
   versao = models.CharField("Versão",max_length=20, unique=True,null=False)
   data_registro = (auto_now_add=True, null=False)
   data_atualizacao = models.DateTimeField(auto_now=True)
   status = models.BooleanField(default=True)
   def __str__(self):
      return self.versao