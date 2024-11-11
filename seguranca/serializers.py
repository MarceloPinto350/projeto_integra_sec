from rest_framework import serializers

from django.db.models import Count

from .models import (AreaNegocial, TipoAplicacao, TipoVarredura, SistemaVarredura, Aplicacao, VersaoAplicacao, ResultadoScan, 
   Configuracao, ArquivoConfiguracao, Relacionamento, AtivoInfraestrutura, ModeloDocumento, TipoAtivoInfraestrutura, Rede, 
   BancoDados, Servico, Servidor, TipoRelacionamento, Varredura
   )

from  django.utils import timezone   
class AreaNegocialSerializer(serializers.ModelSerializer):
   class Meta:
      model = AreaNegocial
      fields = '__all__'

class TipoAplicacaoSerializer(serializers.ModelSerializer):
   class Meta:
      model = TipoAplicacao
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
      fields = '__all__'
      #fields = (
      #  'id','aplicacao_seguranca','tipo_varredura','comando','usa_webhook','aplicacoes'
      #)
  
class AplicacaoSerializer(serializers.ModelSerializer):
   # usando Nested Relatioship: Ruim para muitos registros, pois pode sobrecarregar a API
   #versoes = serializers.PrimaryKeyRelatedField(many=True, read_only=True), 
   #
   # usando Hyperlinked Related Field (recomendado para volume médio de registros)
   # atentar para o view_name que deve ser o mesmo nome da view que define a rota
   #versoes = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='versaoaplicacao-detail')
   #
   # usando PrimaryKey Related Field
   # recomendado para muitos registros pois retorna apenas o id do registro relacionado
   # versoes = serializers.PrimaryKeyRelatedField(many=True, read_only=True) 
   # servicos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
   # servidores = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
   # aplicacoes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
      
   class Meta:
      extra_kwargs = {
         'url_acesso': {'write_only': True},
         #'usuario_servico': {'write_only': True},
         'senha_servico': {'write_only': True},
         'token_acesso': {'write_only': True},         
      }
      cont_versoes = serializers.SerializerMethodField()
      model = Aplicacao
      fields = (
         'id','nome','sigla','descricao','categoria','url_codigo_fonte',
         'data_registro','data_atualizacao','data_descontinuacao',
         #'area_analista_liberacao','abrangencia','area_responsavel','gestor_negocial',
         #'essencial','estrategico','arquitetura','hospedagem','tipo',
         'aplicacao_pai','usuario_servico',
         # campo calculado para contagem de versões de aplicação
         
      )
      # validação de dados na serialização
      # o nome da função deve ser validate_<nome_campo>
      def validate_data_descontinuacao (self, data):
         if data < timezone.now():
            raise serializers.ValidationError('A data de descontinuação não pode ser menor que a data atual.')
         return data
      # extendendo campos serializados
      # def get_cont_versoes(self, obj):
      #    contagem = obj.versoes.aggregate(contagem=Count('id'))
      #    if contagem is None:
      #       return 0
      #    return contagem
      # def ultima_versao(self, obj):
      #    return obj.versoes.last()
            
class VersaoAplicacaoSerializer(serializers.ModelSerializer):
   class Meta:
      model = VersaoAplicacao
      fields = '__all__'

class ResultadoScanSerializer(serializers.ModelSerializer):
   class Meta:
      model = ResultadoScan
      fields = '__all__'
      
class ConfiguracaoSerializer(serializers.ModelSerializer):
   class Meta:
      model = Configuracao
      fields = '__all__'

class ArquivoConfiguracaoSerializer(serializers.ModelSerializer):
   class Meta:
      model = ArquivoConfiguracao
      fields = '__all__'

class RelacionamentoSerializer(serializers.ModelSerializer):
   class Meta:
      model = Relacionamento
      fields = '__all__'

class AtivoInfraestruturaSerializer(serializers.ModelSerializer): 
   class Meta:
      model = AtivoInfraestrutura
      fields = '__all__'

   def validate_data_resultado (self, data):
      if data > timezone.now():
         raise serializers.ValidationError('A data de resultado não pode ser maior que a data atual.')
      return data 
  
class ModeloDocumentoSerializer(serializers.ModelSerializer):
   class Meta:
      model = ModeloDocumento
      fields = '__all__'          

class TipoAtivoInfraestruturaSerializer(serializers.ModelSerializer):   
   class Meta:
      model = TipoAtivoInfraestrutura
      fields = '__all__'    

class RedeSerializer(serializers.ModelSerializer):
   class Meta:
      model = Rede
      fields = '__all__'

class BancoDadosSerializer(serializers.ModelSerializer):
   class Meta:
      model = BancoDados
      fields = '__all__'
      
class ServicoSerializer(serializers.ModelSerializer):
   class Meta:
      model = Servico
      fields = '__all__'
              
class ServidorSerializer(serializers.ModelSerializer):
   class Meta: 
      model = Servidor
      fields = '__all__'         

class TipoRelacionamentoSerializer(serializers.ModelSerializer):
   class Meta:
      model = TipoRelacionamento
      fields = '__all__'

class VarreduraSerializer(serializers.ModelSerializer):
   #aplicacao = AplicacaoSerializer(read_only=True)
   class Meta: 
      model = Varredura
      fields = '__all__'

# classe para tratamento da serialização de resultados das varreduras
class SonarResultSerializer(serializers.ModelSerializer):
   resultado = serializers.JSONField()
   class Meta:
      model = ResultadoScan
      fields = 'resultado'