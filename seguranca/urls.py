from django import views
from django.urls import path

from rest_framework.routers import SimpleRouter

#from sonar_data.views import SonarResultViewSet

from .views import (
      TipoAplicacaoAPIView, TiposAplicacaoAPIView, 
      AplicacaoAPIView, AplicacoesAPIView,
      VersaoAPIView, VersoesAPIView, 
      ResultadoScanAPIView, ResultadosScanAPIView,
      TipoAplicacaoViewSet, 
      AplicacaoViewSet, 
      VersaoViewSet, 
      ResultadoScanViewSet,
      ResultadoViewSet,
      TipoVarreduraViewSet, 
      SistemaVarreduraViewSet)   

# definindo o roteador para facilitar a referencia das APIs
router = SimpleRouter()
router.register('tiposaplicacao',TipoAplicacaoViewSet)
router.register('aplicacoes',AplicacaoViewSet)
router.register('versoes',VersaoViewSet)
router.register('resultadosscan',ResultadoScanViewSet)
#router.register('results',ResultadoViewSet, basename='results')
router.register('tiposvarredura',TipoVarreduraViewSet)
router.register('sistemasvarredura',SistemaVarreduraViewSet)      

# define as rotas para as APIs
urlpatterns = [
      path('tiposaplicacao/', TiposAplicacaoAPIView.as_view(), name='tiposaplicacao'),
      path('tiposaplicacao/<int:pk>/', TipoAplicacaoAPIView.as_view(), name='tipoaplicacao'),

      path('aplicacoes/', AplicacoesAPIView.as_view(), name='aplicacoes'),
      path('aplicacoes/<int:pk>/', AplicacaoAPIView.as_view(), name='aplicacao'),
      path('aplicacoes/<int:aplicacao_pk>/versoes', VersoesAPIView.as_view(), name='aplicacao_versoes'),     
      path('aplicacoes/<int:aplicacao_pk>/versoes/<int:versao_pk>/', VersaoAPIView.as_view(), name='aplicacao_versao'),     

      path('versoes/', VersoesAPIView.as_view(), name='versoes'),
      path('versoes/<int:versao_pk>/', VersaoAPIView.as_view(), name='versao'),
      
      path('resultadosscan/', ResultadosScanAPIView.as_view(), name='resultadosscan'),
      path('resultadosscan/<int:pk>/', ResultadoScanAPIView.as_view(), name='resultadoscan'),
      
      path('resultados/', ResultadoViewSet.as_view({'post':'post'}), name='resultados'),

      #exit
      # path('',views.index,name='index'),
]




