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

#from seguranca import realiza_varredura
from seguranca.utils import varredura,varrer_SAST

from .models import (AreaNegocial,TipoAplicacao,TipoVarredura,SistemaVarredura,Aplicacao,VersaoAplicacao,ResultadoScan,Configuracao,
   ArquivoConfiguracao,ModeloDocumento,AtivoInfraestrutura,Relacionamento,TipoAtivoInfraestrutura,User,Servico,BancoDados,Rede, 
   Servidor,TipoRelacionamento,Varredura
)
from .serializers import (TipoAplicacaoSerializer, AreaNegocialSerializer, AplicacaoSerializer, VersaoAplicacaoSerializer,
   TipoAtivoInfraestruturaSerializer, AtivoInfraestruturaSerializer, ResultadoScanSerializer, TipoVarreduraSerializer, 
   VersaoAplicacaoSerializer, SistemaVarreduraSerializer, ModeloDocumentoSerializer, VarreduraSerializer,
   RedeSerializer, ServidorSerializer, BancoDadosSerializer, ServicoSerializer   
)
from .permissions import EhSuperUsuario

from seguranca.utils import varredura_result, varrer_SCA,varrer_DAST

from django.utils import timezone

#testado o celery para processamento assíncrono
#from celery import shared_task

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
  
class VarreduraViewSet(viewsets.ModelViewSet):  
   permissions_classes = (permissions.DjangoModelPermissions, )
   queryset = Varredura.objects.all()
   serializer_class = VarreduraSerializer
  
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
   """
   ViewSet para processar a varredura de uma aplicação

   Args: Exemplo
      {
         "nome_aplicacao": "DVWA",
         "origem_processamento": "API",
         "sistema_varredura": ["ALL","SAST","DAST","SCA"]
         }
   """
   def post(self, request):
      ########################################################
      # CRIANDO A VARREDURA
      #print ("Inicializando a varredura...")
      vVarredura = varredura.inicializa(request.data)
      serializer =  VarreduraSerializer(data=vVarredura)
      if serializer.is_valid():
         serializer.save()
         #return Response(serializer.data, status=201)
      else:
         return Response(serializer.errors, status=400)
      print (f"Varredura cadastrada: {serializer.data}")
      print()
      ########################################################
      # PROCESSANDO CADA TIPO DE VARREDURA
      aplicacao = Aplicacao.objects.get(pk=serializer.data['aplicacao'])
      # coleta os sistemas de varredura ativos para a aplicação
      versoes = VersaoAplicacao.objects.filter(aplicacao=aplicacao.id)
      lista_versoes = []
      for ver in versoes:  
         lista_versoes.append(ver.id)
      #print (f"Varrendo aplicação {serializer.data['aplicacao']} - {lista_versoes}")
      sistemas_varredura = SistemaVarredura.objects.filter(situacao='ATIVO', aplicacoes__in=lista_versoes)
      #print (f"Sistemas de varredura ativos: {sistemas_varredura}")
      resultado = {}
      if "ALL" == request.data['sistema_varredura']:
         for sist_varr in sistemas_varredura:
            processar = {
                  "aplicacao": aplicacao.nome,
                  "aplicacao_sigla": aplicacao.sigla,     
                  "aplicacao_id": aplicacao.id,
                  "url_codigo_fonte": aplicacao.url_codigo_fonte,
                  "varredura": serializer.data['id'],
                  "sistema_varredura": sist_varr.id,
                  "sist_varredura_ip_acesso": sist_varr.ip_acesso,
                  "sist_varredura_host": sist_varr.aplicacao_seguranca.url_codigo_fonte,
                  "sist_varredura_comando": sist_varr.comando,
                  "sist_varredura_webhook": sist_varr.usa_webhook,
                  "sist_varredura_tipo": sist_varr.tipo_varredura,
                  "sist_varredura_sigla_tipo": sist_varr.tipo_varredura.nome,
                  "sist_varredura_usuario": sist_varr.usuario, #sist_varr.aplicacao_seguranca.usuario_servico, 
                  "sist_varredura_senha": sist_varr.senha, #sist_varr.aplicacao_seguranca.senha_servico,
                  "sist_varredura_token": sist_varr.token,
                  "caminho_resultado": f"app/{aplicacao.sigla}_{sist_varr.tipo_varredura.nome}_{sist_varr.id}.json"
               }
            #print (f"Vai processar os tipos de varredura: {request.data['sistema_varredura']}")
            #print (f"Tipo de varredura a ser processado: {sist_varr.tipo_varredura.nome}")
            #print (f"Tipo de varredura a ser processado está na lista: {sist_varr.tipo_varredura.nome} - {sist_varr.tipo_varredura.nome in request.data['sistema_varredura']}")
            # Define o que será processado
            if "SAST" == sist_varr.tipo_varredura.nome:
               # realiza a varredura
               print (f"Vai processar: SAST")
               resultado = varrer_SAST.processa(processar)
            elif "SCA" == sist_varr.tipo_varredura.nome:
               print (f"Vai processar: SCA")
               resultado = varrer_SCA.processa(processar)
            elif "DAST" == sist_varr.tipo_varredura.nome:
               # realiza a varredura
               print (f"Vai processar: DAST")
               resultado = varrer_DAST.processa(processar)
            else: 
               print(f"Tipo de varredura não implementado: {sist_varr.tipo_varredura.nome}")
      else:
         for sist_varr in sistemas_varredura:
            processar = {
                  "aplicacao": aplicacao.nome,
                  "aplicacao_sigla": aplicacao.sigla,     
                  "aplicacao_id": aplicacao.id,
                  "url_codigo_fonte": aplicacao.url_codigo_fonte,
                  "varredura": serializer.data['id'],
                  "sistema_varredura": sist_varr.id,
                  "sist_varredura_ip_acesso": sist_varr.ip_acesso,
                  "sist_varredura_host": sist_varr.aplicacao_seguranca.url_codigo_fonte,
                  "sist_varredura_comando": sist_varr.comando,
                  "sist_varredura_webhook": sist_varr.usa_webhook,
                  "sist_varredura_tipo": sist_varr.tipo_varredura,
                  "sist_varredura_sigla_tipo": sist_varr.tipo_varredura.nome,
                  "sist_varredura_usuario": sist_varr.usuario, #sist_varr.aplicacao_seguranca.usuario_servico, 
                  "sist_varredura_senha": sist_varr.senha, #sist_varr.aplicacao_seguranca.senha_servico,
                  "sist_varredura_token": sist_varr.token,
                  "caminho_resultado": f"app/{aplicacao.sigla}_{sist_varr.tipo_varredura.nome}_{sist_varr.id}.json"
               }
            # print (f"Vai processar os tipos de varredura: {request.data['sistema_varredura']}")
            # print (f"Tipo de varredura a ser processado: {sist_varr.tipo_varredura.nome}")
            # print (f"Tipo de varredura a ser processado está na lista: {sist_varr.tipo_varredura.nome} - {sist_varr.tipo_varredura.nome in request.data['sistema_varredura']}")
            # Define o que será processado
            if sist_varr.tipo_varredura.nome in request.data['sistema_varredura']:
               if "SAST" == sist_varr.tipo_varredura.nome:
                  # realiza a varredura
                  print (f"Vai processar: SAST")
                  resultado = varrer_SAST.processa(processar)
               elif "SCA" == sist_varr.tipo_varredura.nome:
                  print (f"Vai processar: SCA")
                  resultado = varrer_SCA.processa(processar)
               elif "DAST" == sist_varr.tipo_varredura.nome:
                  # realiza a varredura
                  print (f"Vai processar: DAST")
                  resultado = varrer_DAST.processa(processar)
               else: 
                  print(f"Tipo de varredura não implementado: {sist_varr.tipo_varredura.nome}")
         
      
      # Ajustar a varredura para concluir
      try:
         vVarredura = Varredura.objects.get(pk=resultado['varredura'])
         vVarredura.situacao = 'CONCLUÍDA'
         vVarredura.data_fim = timezone.now()
         vVarredura.save()
      except Exception as e:
         print(f'Erro ao concluir a varredura: {e}')
         vVarredura = Varredura.objects.get(pk=resultado['erro'])
         vVarredura.situacao = 'FALHA'
         vVarredura.data_fim = timezone.now()
         vVarredura.save()
      
      try:  
         resultado = {
            "varredura_id": vVarredura.pk,
            "data_resultado": vVarredura.data_fim,
            "origem_varredura": vVarredura.origem,
            "aplicacao": vVarredura.aplicacao.nome,
            "situacao": vVarredura.situacao
         }
         return Response(resultado,status=201)   
      except Exception as e:
         return Response(f'Erro ao processar o resultado: {e}',status=500)


# montagem do grafo de relacionamentos
class GrafoViewSet (viewsets.ViewSet):
   """
   ViewSet para processar a montagem do grafo de relacionamentos

   Args: Exemplo
      {
         "sigla_aplicacao": "DVWA",
      }
   """
   def get(self, request):
      if request.method == 'POST':
        aplicacao_selecionada = Aplicacao.objects.get(sigla=request.data['sigla_aplicacao'])
        # Lógica para buscar os relacionamentos e montar o JSON
        relacionamentos = Relacionamento.objects.filter(aplicacao_id=aplicacao_selecionada.id)
        data = []
        # ... (montar a estrutura do JSON para o D3.js)
        return JsonResponse(data, safe=False)
      else:
        # Renderizar o template inicial com o formulário de seleção da aplicação
        return render(request, 'grafo.html')