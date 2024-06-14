from rest_framework import serializers

from django.db.models import Count

from .models import Aplicacao, ResultadoScan, TipoAplicacao, VersaoAplicacao, TipoVarredura, SistemaVarredura

class TipoAplicacaoSerializer(serializers.ModelSerializer):
   class Meta:
      model = TipoAplicacao
      fields = '__all__'

class VersaoAplicacaoSerializer(serializers.ModelSerializer):
   class Meta:
      model = VersaoAplicacao
      fields = '__all__'

class TipoVarreduraSerializer(serializers.ModelSerializer):  
   class Meta:
      model = TipoVarredura
      fields = '__all__'

class SistemaVarreduraSerializer(serializers.ModelSerializer):
   #aplicacoes = TipoAplicacaoSerializer(many=True, read_only=True) 
   #tipos_varredura = TipoVarreduraSerializer(many=True, read_only=True)  
   tipos_varredura = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  
   class Meta:
      model = SistemaVarredura
      fields = (
        'id','nome','descricao','url','usuario','senha','token','status',
         # campo para serialização dos tipos de varredura
         'aplicacoes','tipos_varredura'
      )
  
class AplicacaoSerializer(serializers.ModelSerializer):
   # usando Nested Relatioship: Ruim para muitos registros, pois pode sobrecarregar a API
   #versoes = VersaoAplicacaoSerializer(many=True, read_only=True,) 
   #
   # usando Hyperlinked Related Field (recomendado para volume médio de registros)
   # atentar para o view_name que deve ser o mesmo nome da view que define a rota
   #versoes = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='versaoaplicacao-detail')
   #
   # usando PrimaryKey Related Field
   # recomendado para muitos registros pois retorna apenas o id do registro relacionado
   versoes = serializers.PrimaryKeyRelatedField(many=True, read_only=True) 
   
   class Meta:
      extra_kwargs = {
         'url_acesso': {'write_only': True},
         'usuario_servico': {'write_only': True},
         'senha_servico': {'write_only': True},
         'token_acesso': {'write_only': True},         
      }
      cont_versoes = serializers.SerializerMethodField()
      model = Aplicacao
      fields = (
         'id','nome','sigla','descricao','categoria','url_fonte',
         'data_registro','data_atualizacao','data_descontinuacao',
         #'area_analista_liberacao','abrangencia','area_responsavel','gestor_negocial',
         #'essencial','estrategico','arquitetura','hospedagem',
         'tipo','url_acesso','aplicacao_pai',
         'usuario_servico','senha_servico','token_acesso',
         # campo para serialização de versões de aplicação
         'versoes' 
         # campo calculado para contagem de versões de aplicação
         #,'cont_versoes'
      )
      # validação de dados na serialização
      # o nome da função deve ser validate_<nome_campo>
      def validate_data_descontinuacao (self, data):
         if data < timezone.now():
            raise serializers.ValidationError('A data de descontinuação não pode ser menor que a data atual.')
         return data
      # extendendo campos serializados
      def get_cont_versoes(self, obj):
         contagem = obj.versoes.aggregate(contagem=Count('id'))
         if contagem is None:
            return 0
         return contagem
      
      
class ResultadoScanSerializer(serializers.ModelSerializer):
   class Meta:
      model = ResultadoScan
      fields = '__all__'
      
   def validate_data_resultado (self, data):
      if data > timezone.now():
         raise serializers.ValidationError('A data de resultado não pode ser maior que a data atual.')
      return data
   
# classe para tratamento da serialização de resultados das varreduras
class SonarResultSerializer(serializers.ModelSerializer):
   resultado = serializers.JSONField()
   class Meta:
      model = ResultadoScan
      fields = 'resultado'