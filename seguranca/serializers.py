from rest_framework import serializers

from .models import Aplicacao, ResultadoScan, TipoAplicacao

class TipoAplicacaoSerializer(serializers.ModelSerializer):
   class Meta:
      model = TipoAplicacao
      fields = '__all__'


class AplicacaoSerializer(serializers.ModelSerializer):
   class Meta:
      extra_kwargs = {
         'url_acesso': {'write_only': True},
         'usuario_servico': {'write_only': True},
         'senha_servico': {'write_only': True},
         'token_acesso': {'write_only': True},
      }
      model = Aplicacao
      fields = (
         'nome','sigla','descricao','categoria','url_fonte',
         'data_registro','data_atualizacao','data_descontinuacao',
         #'area_analista_liberacao','abrangencia','area_responsavel','gestor_negocial',
         #'essencial','estrategico','arquitetura','hospedagem',
         'tipo','url_acesso','aplicacao_pai',
         'usuario_servico','senha_servico','token_acesso'
      )

        
class ResultadoScanSerializer(serializers.ModelSerializer):
   class Meta:
      model = ResultadoScan
      fields = '__all__'        