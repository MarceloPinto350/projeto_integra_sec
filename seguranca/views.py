from rest_framework import generics 

from .models import TipoAplicacao, Aplicacao, ResultadoScan
from .serializers import TipoAplicacaoSerializer, AplicacaoSerializer, ResultadoScanSerializer

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


# para listar e criar novos registros de resultados de scan
class ResultadosScanAPIView(generics.ListCreateAPIView):
   queryset = ResultadoScan.objects.all()
   serializer_class = ResultadoScanSerializer

# para recuperar, atualizar e deletar um registro de resultado de scan
class ResultadoScanAPIView(generics.RetrieveUpdateDestroyAPIView):
   queryset = ResultadoScan.objects.all()
   serializer_class = ResultadoScanSerializer
