from django.shortcuts import render
from rest_framework import generics 
from rest_framework.generics import get_object_or_404
from rest_framework import status

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action 
from rest_framework.response import Response
from rest_framework import mixins 

from rest_framework import permissions 

from .models import TipoAplicacao, Aplicacao, ResultadoScan, VersaoAplicacao, TipoVarredura, SistemaVarredura
from .serializers import (TipoAplicacaoSerializer, AplicacaoSerializer,
   ResultadoScanSerializer, VersaoAplicacaoSerializer, 
   TipoVarreduraSerializer, SistemaVarreduraSerializer
)
from .permissions import EhSuperUsuario

#import jsonpath
from integracao import varredura_result



"""
API Versão 1.0
"""
# classe genérica para listar e criar novos registros de tipos de aplicação
# generics.ListCreateAPIView - lista e cria novos registros
# generics.RetrieveUpdateDestroyAPIView - recupera, atualiza e deleta um registro registro   
# para listar e criar novos registros de tipos de aplicação 
class TiposAplicacaoAPIView(generics.ListCreateAPIView):
   queryset = TipoAplicacao.objects.all()
   serializer_class = TipoAplicacaoSerializer

# para recuperar, atualizar e deletar um registro de tipo de aplicação
class TipoAplicacaoAPIView(generics.RetrieveUpdateDestroyAPIView):
   queryset = TipoAplicacao.objects.all()
   serializer_class = TipoAplicacaoSerializer

# para listar e criar novos registros de aplicações
class AplicacoesAPIView(generics.ListCreateAPIView):
   queryset =  Aplicacao.objects.all()
   serializer_class = AplicacaoSerializer

# para recuperar, atualizar e deletar um registro de aplicação      
class AplicacaoAPIView(generics.RetrieveUpdateDestroyAPIView):
   queryset =  Aplicacao.objects.all()
   serializer_class = AplicacaoSerializer

# para listar e criar novos registros de aplicações
class VersoesAPIView(generics.ListCreateAPIView):
   queryset =  VersaoAplicacao.objects.all()
   serializer_class = VersaoAplicacaoSerializer
   # trata a filtragem de registros de versões de aplicação
   # conforme a rota acessada (aplicacoes/<int:aplicacao_pk>/versoes/<int:versao_pk>/)
   def get_queryset(self):
      if self.kwargs.get('aplicacao_pk'):
         return self.queryset.filter(aplicacao_id=self.kwargs.get('aplicacao_pk'))
      return self.queryset.all()

# para recuperar, atualizar e deletar um registro de aplicação      
class VersaoAPIView(generics.RetrieveUpdateDestroyAPIView):
   queryset =  VersaoAplicacao.objects.all()
   serializer_class = VersaoAplicacaoSerializer
   # alterar o método get_queryset para filtrar registros de versões de aplicação
   def get_object (self):
      if self.kwargs.get('aplicacao_pk'):
         return get_object_or_404(self.get_queryset(),
                                  aplicacao_id=self.kwargs.get('aplicacao_pk'),
                                  pk=self.kwargs.get('versao_pk'))
      return get_object_or_404(self.get_queryset(),pk=self.kwargs.get('versao_pk'))

# para listar e criar novos registros de resultados de scan
class ResultadosScanAPIView(generics.ListCreateAPIView):
   queryset = ResultadoScan.objects.all()
   serializer_class = ResultadoScanSerializer

# para recuperar, atualizar e deletar um registro de resultado de scan
class ResultadoScanAPIView(generics.RetrieveUpdateDestroyAPIView):
   queryset = ResultadoScan.objects.all()
   serializer_class = ResultadoScanSerializer


"""
API Versão 2.0
"""

class TipoAplicacaoViewSet(viewsets.ModelViewSet):
   permissions_classes = (
      EhSuperUsuario,
      permissions.DjangoModelPermissions, 
   )
   queryset = TipoAplicacao.objects.all()
   serializer_class = TipoAplicacaoSerializer
   
class AplicacaoViewSet(viewsets.ModelViewSet):
   queryset = Aplicacao.objects.all()
   serializer_class = AplicacaoSerializer   
   # criando uma ação personalizada para listar as versões de uma aplicação
   # pesquisar as versões de uma aplicação
   @action(detail=True, methods=['get'])
   def versoes(self, request, pk=None):
      # para alterar o comportamento padrão de paginação definido no settings.py que não afeta esta ação
      self.pagination_class.page_size = 1
      versoes = VersaoAplicacao.objects.filter(aplicacao_id=pk)
      page = self.paginate_queryset(versoes)
      if page is not None:
         serializer = VersaoAplicacaoSerializer(page, many=True)
         return self.get_paginated_response(serializer.data)
      serializer = VersaoAplicacaoSerializer(versoes, many=True)
      # comentadas a linhas abaixo pq foi subtituído pela declaração da paginação
      # aplicacao = self.get_object() 
      # observer que versoes é um campo relacionado conforme models.py
      #serializer = VersaoAplicacaoSerializer(aplicacao.versoes.all(), many=True) 
      return Response(serializer.data)
   # 
   
"""
# comentado para mostrar a mesma coisa feita através do uso de mixins para modificar conportamento padrão
# a ser utilizado conforme a necessidades
class VersaoViewSet(viewsets.ModelViewSet):
   queryset = VersaoAplicacao.objects.all()
   serializer_class = VersaoAplicacaoSerializer
"""
class VersaoViewSet( 
   # caso queira não disponibilizar todas as ações, pode-se comentar a que vc deseja bloquear
   mixins.ListModelMixin,
   mixins.CreateModelMixin,
   mixins.RetrieveModelMixin,
   mixins.UpdateModelMixin,
   mixins.DestroyModelMixin,
   viewsets.GenericViewSet
   ):
   permissions_classes = (permissions.DjangoModelPermissions, )
   queryset = VersaoAplicacao.objects.all()
   serializer_class = VersaoAplicacaoSerializer

class TipoVarreduraViewSet(viewsets.ModelViewSet):
   queryset = TipoVarredura.objects.all()
   serializer_class = TipoVarreduraSerializer

class SistemaVarreduraViewSet(viewsets.ModelViewSet):
   permissions_classes = (permissions.DjangoModelPermissions, )
   queryset = SistemaVarredura.objects.all()
   serializer_class = SistemaVarreduraSerializer

class ResultadoScanViewSet(viewsets.ModelViewSet):
   queryset = ResultadoScan.objects.all()
   serializer_class = ResultadoScanSerializer
   
class ResultadoViewSet(viewsets.ViewSet):
   def post(self, request):
      # validar se o valor recebido é um JSON
      #serializer =  ResultadoViewSet(data=request.data)
      #serializer.is_valid(raise_exception=True)
      # recebe dados do SonarQube e envia para processamento
      resultado = varredura_result.processa_resultado(request.data)
      # validar o serializer e salvar dados no BD
      serializer =  ResultadoScanSerializer(data=resultado)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=201)
      else:
         return Response(serializer.errors, status=400)
      

def index(request):
   """
   View function para a página inicial
   """
   num_aplicacoes = Aplicacao.objects.all().count()
   num_varreduras = ResultadoScan.objects.all().count()
   
   context = { 
      'num_aplicacoes': num_aplicacoes,
      'num_varreduras': num_varreduras,          
   }
   
   return render(request, index.htm, context=context)
   
   
