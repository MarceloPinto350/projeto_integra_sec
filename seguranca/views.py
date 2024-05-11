from rest_framework import generics 

from .models import TipoAplicacao, Aplicacao, ResultadoScan
from .serializers import TipoAplicacaoSerializer, AplicacaoSerializer, ResultadoScanSerializer

# classe genérica para listar e criar novos registros de tipos de aplicação
# generics.ListCreateAPIView - lista e cria novos registros
# generics.RetrieveUpdateDestroyAPIView - recupera, atualiza e deleta um registro registro   
# para mais informações sobre as classes genéricas do Django Rest Framework, acesse: https://www.django-rest-framework.org/api-guide/generics/
class TiposAplicacaoAPIView(generics.ListCreateAPIView):
   queryset = TipoAplicacao.objects.all()
   serializer_class = TipoAplicacaoSerializer



class TipoAplicacaoAPIView(generics.RetrieveUpdateDestroyAPIView):
   queryset = TipoAplicacao.objects.all()
   serializer_class = TipoAplicacaoSerializer


class AplicacoesAPIView(generics.ListCreateAPIView):
   queryset =  Aplicacao.objects.all()
   serializer_class = AplicacaoSerializer

      
class AplicacaoAPIView(generics.RetrieveUpdateDestroyAPIView):
   queryset =  Aplicacao.objects.all()
   serializer_class = AplicacaoSerializer


class ResultadosScanAPIView(generics.ListCreateAPIView):
   queryset = ResultadoScan.objects.all()
   serializer_class = ResultadoScanSerializer


class ResultadoScanAPIView(generics.RetrieveUpdateDestroyAPIView):
   queryset = ResultadoScan.objects.all()
   serializer_class = ResultadoScanSerializer
