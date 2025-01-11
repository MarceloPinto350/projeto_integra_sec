from django import forms

from .models import SistemaVarredura, Aplicacao, VersaoAplicacao, AtivoInfraestrutura, Rede, BancoDados

# implementação do form para filtrar as aplicações de segurança e as aplicações de varredura, 
# excluindo-se as aplicações de segurança
class SistemaVarreduraForm(forms.ModelForm):
   class Meta:
      model = SistemaVarredura
      fields = '__all__'
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      #self.fields['aplicacao_seguranca'].queryset = Aplicacao.objects.filter(tipo_aplicacao='Segurança')
      self.fields['aplicacao_seguranca'].queryset = Aplicacao.objects.filter(tipo_aplicacao__nome='Segurança')
      self.fields['aplicacoes'].queryset = VersaoAplicacao.objects.exclude(aplicacao__tipo_aplicacao__nome='Segurança')

# implementação do form para filtrar os ativos de infraestrutura, incluindo-se apenas os tipo de ativo banco de dados
class BancoDadosForm(forms.ModelForm):
    class Meta:
        model = BancoDados
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ativo_infraestrutura'].queryset = AtivoInfraestrutura.objects.filter(tipo_ativo__nome='Banco de dados')

class AplicacaoForm(forms.ModelForm):
    class Meta:
        model = Aplicacao
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['aplicacao_pai'].queryset = Aplicacao.objects.filter(tipo_aplicacao__nome='Sistema')
        
class RedeForm(forms.ModelForm):
    class Meta:
        model = Rede
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ativos_infraestrutura'].queryset = AtivoInfraestrutura.objects.filter(tipo_ativo__nome='Rede')