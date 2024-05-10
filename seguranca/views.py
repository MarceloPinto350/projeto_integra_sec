from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import TipoAplicacao,Aplicacao, ResultadoScan
from .serializers import TipoAplicacaoSerializer,AplicacaoSerializer, ResultadoScanSerializer
#from .scanners import sonarQube #, owaspZap, owaspDependencyCheck

# Importações das bibliotecas para as ferramentas de segurança
#import sonarQube
#import owaspZap
#import owaspDependencyCheck

class TipoAplicacaoAPIView(APIView):
   """
   API da Classe TipoAplicacao para obter e criar tipos de aplicação
   """
   def get(self, request):
      #print(request.user) # visualiza o usuário que fez a requisição ...
      print(dir(request)) # visualiza todos os dados do request
      tiposaplicacao = TipoAplicacao.objects.all()
      serializer= TipoAplicacaoSerializer(tiposaplicacao, many=True)
      return Response(serializer.data)
   
   def post(self, request):
      serializer = TipoAplicacaoSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      

class AplicacaoAPIView(APIView):
   """
   API da Classe Aplicação para obter e criar aplicações
   """
   def get(self, request):
      aplicacoes = Aplicacao.objects.all()    
      serializer = AplicacaoSerializer(aplicacoes, many=True)
      return Response(serializer.data)
      
   def post(self, request):
      serializer = AplicacaoSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data,status=status.HTTP_201_CREATED)
      else:
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

      
class ResultadoScanAPIView(APIView):
   """
   API para obter os resultados da varredura de segurança
   """
   def post(self, request):
      id_aplicacao = request.data['id_aplicacao']
      aplicacao = Aplicacao.objects.get(pk=id_aplicacao)
      # Executar varredura SAST com SonarQube
      sonar_result = sonarQube.scan(aplicacao.url_acesso, aplicacao.url_fonte)
      # Executar varredura DAST com OWASP ZAP
#      owaspZap_result = owaspZap.scan(aplicacao.url_acesso)
      # Executar varredura SCA com OWASP Dependency Check
#      owaspDC_result = owaspDependencyCheck.scan(aplicacao.url_fonte)
      # opção para combinar os rsultados em um único objeto
#      scan_result#         'sonarQube':sonar_result,
#         'owaspZap':owaspZap_result,
#         'owaspDependencyCheck':owaspDC_result
#      }
      # salvar o resultado da varredura no banco de dados
      resultado_scan = ResultadoScan.object.create (aplicacao=aplicacao, resultado=scan_result)
      # serializar o resultado da varredura
#      serializer = ScanResultSerializer(resultado_scan) 
#      if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#      else:
#         return Response(serializer.errors)


