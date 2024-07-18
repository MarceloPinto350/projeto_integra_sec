from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.views import generic 

from rest_framework import generics 
from rest_framework.generics import get_object_or_404
from rest_framework import status

#from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action 
from rest_framework.response import Response
from rest_framework import mixins 

from rest_framework import permissions 

from .models import (TipoAplicacao, AreaNegocial, Aplicacao, VersaoAplicacao, TipoAtivoInfraestrutura, User,
   AtivoInfraestrutura, ResultadoScan, TipoVarredura, SistemaVarredura, TipoModeloDocumento, ModeloDocumento,
   Rede, Servidor, BancoDados, Servico
)
from .serializers import (TipoAplicacaoSerializer, AreaNegocialSerializer, AplicacaoSerializer, VersaoAplicacaoSerializer,
   TipoAtivoInfraestruturaSerializer, AtivoInfraestruturaSerializer, ResultadoScanSerializer, TipoVarreduraSerializer, 
   VersaoAplicacaoSerializer, SistemaVarreduraSerializer, TipoModeloDocumentoSerializer, ModeloDocumentoSerializer,
   RedeSerializer, ServidorSerializer, BancoDadosSerializer, ServicoSerializer   
)
from .permissions import EhSuperUsuario

#import jsonpath
#from integracao import varredura_result
from seguranca.utils import varredura_result, realiza_varredura


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
Utilizando viewsets para criar uma API REST por ter maior flexibilidade e facilidade de uso
"""

class TipoAplicacaoViewSet(viewsets.ModelViewSet):
   permissions_classes = (
      EhSuperUsuario,
      permissions.DjangoModelPermissions, 
   )
   queryset = TipoAplicacao.objects.all()
   serializer_class = TipoAplicacaoSerializer
   
class AreaNegocialViewSet(viewsets.ModelViewSet):
   queryset = AreaNegocial.objects.all()
   serializer_class = AreaNegocialSerializer
   
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
   # criando uma ação personalizada para listar última versão de uma aplicação
   def ultima_versao(self, request, pk=None):
      ultima_versao = self.get_object(0)
      serializer = VersaoAplicacaoSerializer(ultima_versao)
      return Response(serializer.data)

# comentado para mostrar a mesma coisa feita através do uso de mixins para modificar conportamento padrão
# a ser utilizado conforme a necessidades
#class VersaoViewSet(viewsets.ModelViewSet):
#   queryset = VersaoAplicacao.objects.all()
#   serializer_class = VersaoAplicacaoSerializer


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

class TipoAtivoInfraestruturaViewSet(viewsets.ModelViewSet):   
   queryset = TipoAtivoInfraestrutura.objects.all()
   serializer_class = TipoAtivoInfraestruturaSerializer
   
class AtivoInfraestruturaViewSet(viewsets.ModelViewSet):
   permissions_classes = (permissions.DjangoModelPermissions, )
   queryset = AtivoInfraestrutura.objects.all()
   serializer_class = AtivoInfraestruturaSerializer


# classes para manipulação dos ativos de inraestrutura]
class RedeViewSet(viewsets.ModelViewSet):
   permissions_classes = (permissions.DjangoModelPermissions, )
   queryset = Rede.objects.all()
   serializer_class = RedeSerializer

class ServidorViewSet(viewsets.ModelViewSet):
   permissions_classes = (permissions.DjangoModelPermissions, )
   queryset = Servidor.objects.all()
   serializer_class = ServidorSerializer
   
class BancoDadosViewSet(viewsets.ModelViewSet):  
   permissions_classes = (permissions.DjangoModelPermissions, )
   queryset = BancoDados.objects.all()
   serializer_class = BancoDadosSerializer
   
class ServicoViewSet(viewsets.ModelViewSet):  
   permissions_classes = (permissions.DjangoModelPermissions, )
   queryset = Servico.objects.all()
   serializer_class = ServicoSerializer      

class ResultadoScanViewSet(viewsets.ModelViewSet):
   permissions_classes = (permissions.DjangoModelPermissions, )
   queryset = ResultadoScan.objects.all()
   serializer_class = ResultadoScanSerializer
   
class TipoVarreduraViewSet(viewsets.ModelViewSet):
   queryset = TipoVarredura.objects.all()
   serializer_class = TipoVarreduraSerializer

class SistemaVarreduraViewSet(viewsets.ModelViewSet):
   permissions_classes = (permissions.DjangoModelPermissions, )
   queryset = SistemaVarredura.objects.all()
   serializer_class = SistemaVarreduraSerializer

class TipoModeloDocumentoViewSet(viewsets.ModelViewSet):
   queryset = TipoModeloDocumento.objects.all()
   serializer_class = TipoModeloDocumentoSerializer
   
class ModeloDocumentoViewSet(viewsets.ModelViewSet):
   permissions_classes = (permissions.DjangoModelPermissions, )
   queryset = ModeloDocumento.objects.all()
   serializer_class = ModeloDocumento

####   
# visões das páginas web 
####
def index(request):
   """
   View function para a página inicial
   """
   aplicacao_list = Aplicacao.objects.order_by("nome")[:5]
   #num_varreduras = ResultadoScan.objects.all().count()
   #num_ativos = AtivoInfraestrutura.objects.all().count()
   template = loader.get_template("index.html")
   
   context = { 
      "aplicacao_list": aplicacao_list,
   }  
   return HttpResponse(template.render(context,request))
   
def appdetail(request, aplicacao_id):
   """
   View function para a página de detalhes de uma aplicação
   """
   aplicacao = get_object_or_404(Aplicacao, pk=aplicacao_id)
   return render(request, 'appdetail.html', {'aplicacao': aplicacao})

def api_users (request):
   """
   View function para a página de usuários
   """
   users = User.objects.all()
   data = [
      {'username': user.username}
      for user in users
   ]
   response = {'data': data}
   return JsonResponse(response)
   
# classe genérica para listar e criar novos registros de tipos de aplicação
class IndexView(generic.ListView):  
   template_name = 'index.html'
   context_object_name = 'aplicacao_list'
   
   def get_queryset(self):
      """Retorna todas as aplicações."""
      return Aplicacao.objects.order_by("nome")

class DetailView(generic.DetailView):
   model = Aplicacao
   template_name = 'appdetail.html'
 
#### 
# visões para chamadas de APIs para processamento das varreduras
####
# Webhook para chamada da API pelo SonarQube
#path('resultados/', ResultadoViewSet.as_view({'post':'post'}), name='resultados'),
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
      
 
# classe que deverá ser utilizada para a página de varredura das aplicações  
class VarrerViewSet(viewsets.ViewSet):
   def post(self, request):
      aplicacao = Aplicacao.objects.get(pk=request.data['aplicacao'])
      print(f"Varrendo aplicação {aplicacao.nome}")
      ultima_versao = aplicacao.ultima_versao()
      print(f"Última versão: {ultima_versao.nome_versao}")
      
      resultado = {
         "Aplicacao": aplicacao.nome,
         "Versao": ultima_versao.nome_versao
      }
      # validar o serializer e salvar dados no BD
      
      serializer =  serializer(data=resultado)
      try:
         realiza_varredura()
         
      #if serializer.is_valid():
         return Response(serializer.data, status=201)
      #else:
      except Exception as e:
         return Response(serializer.errors, status=400)
   """
   View function para a página de varredura
   """
   