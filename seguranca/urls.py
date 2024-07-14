#from django import views
from django.urls import path

from . import views

from rest_framework.routers import SimpleRouter

#from sonar_data.views import SonarResultViewSet

from .views import (
      DetailView, IndexView, TipoAplicacaoAPIView, TiposAplicacaoAPIView, 
      AplicacaoAPIView, AplicacoesAPIView,
      VersaoAPIView, VersoesAPIView, 
      ResultadoScanAPIView,ResultadosScanAPIView,
      TipoAplicacaoViewSet,AreaNegocialViewSet,AplicacaoViewSet,
      VersaoViewSet,TipoAtivoInfraestruturaViewSet,AtivoInfraestruturaViewSet,
      ResultadoScanViewSet,ResultadoViewSet,TipoVarreduraViewSet,VarrerViewSet,
      SistemaVarreduraViewSet,TipoModeloDocumentoViewSet,ModeloDocumentoViewSet)   

# definindo o roteador para facilitar a referencia das APIs
router = SimpleRouter()
router.register('tiposaplicacao',TipoAplicacaoViewSet)
router.register('areasnegociais',AreaNegocialViewSet)
router.register('aplicacoes',AplicacaoViewSet)
router.register('versoes',VersaoViewSet)
router.register('versoes',TipoAtivoInfraestruturaViewSet)
router.register('versoes',AtivoInfraestruturaViewSet)
router.register('resultadosscan',ResultadoScanViewSet)
#router.register('results',ResultadoViewSet, basename='results')
router.register('tiposvarredura',TipoVarreduraViewSet)
router.register('sistemasvarredura',SistemaVarreduraViewSet)      
router.register('versoes',TipoModeloDocumentoViewSet)
router.register('versoes',ModeloDocumentoViewSet)

# define as rotas para as APIs
urlpatterns = [
      #path('tiposaplicacao/', TiposAplicacaoAPIView.as_view(), name='tiposaplicacao'),
      #path('tiposaplicacao/<int:pk>/', TipoAplicacaoAPIView.as_view(), name='tipoaplicacao'),

      #path('aplicacoes/', AplicacoesAPIView.as_view(), name='aplicacoes'),
      #path('aplicacoes/<int:pk>/', AplicacaoAPIView.as_view(), name='aplicacao'),
      #path('aplicacoes/<int:aplicacao_pk>/versoes', VersoesAPIView.as_view(), name='aplicacao_versoes'),     
      #path('aplicacoes/<int:aplicacao_pk>/versoes/<int:versao_pk>/', VersaoAPIView.as_view(), name='aplicacao_versao'),     

      #path('versoes/', VersoesAPIView.as_view(), name='versoes'),
      #path('versoes/<int:versao_pk>/', VersaoAPIView.as_view(), name='versao'),
      
      #path('resultadosscan/', ResultadosScanAPIView.as_view(), name='resultadosscan'),
      #path('resultadosscan/<int:pk>/', ResultadoScanAPIView.as_view(), name='resultadoscan'),
      
      path('resultados/', ResultadoViewSet.as_view({'post':'post'}), name='resultados'),
      path('varrer/', VarrerViewSet.as_view({'post':'post'}), name='varrer'),

      # Visões das aplicações
      #path('aplicacoes/', views.index, name='index'),
      #path('aplicacao/<int:aplicacao_id>/', views.appdetail, name='appdetail'),
      
      path('aplicacoes/', IndexView.as_view(), name='index'),
      #path('aplicacao/<int:aplicacao_id>/', DetailView.as_view({'appdetail'})),
      path('aplicacao/<int:aplicacao_id>/', views.appdetail, name='appdetail'),
      
      
      
      
]




