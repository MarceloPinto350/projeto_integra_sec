from django.urls import path

from .views import  TipoAplicacaoAPIView, AplicacaoAPIView

# define as rotas para as APIs
urlpatterns = [
      path('tiposaplicacao/', TipoAplicacaoAPIView.as_view(), name='tiposaplicacao'),
      path('aplicacoes/', AplicacaoAPIView.as_view(), name='aplicacoes'),
      #path('scan/', ScanView.as_view(), name='scan'),
]
