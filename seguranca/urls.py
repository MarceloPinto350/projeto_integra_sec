from django.urls import path

from .views import  TipoAplicacaoAPIView, TiposAplicacaoAPIView, AplicacaoAPIView, AplicacoesAPIView, ResultadoScanAPIView, ResultadosScanAPIView

# define as rotas para as APIs
urlpatterns = [
      path('tiposaplicacao/', TiposAplicacaoAPIView.as_view(), name='tiposaplicacao'),
      path('aplicacoes/', AplicacoesAPIView.as_view(), name='aplicacoes'),
      path('resultadosscan/', ResultadosScanAPIView.as_view(), name='resultadosscan'),
      path('tiposaplicacao/<int:pk>/', TipoAplicacaoAPIView.as_view(), name='tipoaplicacao'),
      path('aplicacoes/<int:pk>/', AplicacaoAPIView.as_view(), name='aplicacao'),
      path('resultadosscan/<int:pk>/', ResultadoScanAPIView.as_view(), name='resultadoscan'),
]
