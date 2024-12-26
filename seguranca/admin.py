from django.contrib import admin
from .models import (AreaNegocial, TipoAplicacao, TipoVarredura, SistemaVarredura, Aplicacao, VersaoAplicacao, Configuracao, 
    ModeloDocumento, ArquivoConfiguracao, Configuracao, TipoAtivoInfraestrutura, AtivoInfraestrutura, Relacionamento, 
    TipoRelacionamento, Servico, Servidor, Rede, BancoDados
    )

#class CustomAdminSite(admin.AdminSite):
#    site_header = 'Sistema de integração de segurança de aplicações - SISAP'
#    site_title = 'Sistema de integração de segurança de aplicações - SISAP'
#    index_title = 'Bem-vindo ao SISAP'
#admin.site = CustomAdminSite()

@admin.register(AreaNegocial)
class AreaNegocialAdmin (admin.ModelAdmin):
    list_display = ('nome','sigla','id_sigep','ativa')
    list_display_icons = True
    list_per_page = 10

@admin.register(TipoAplicacao)
class TipoAplicacaoAdmin (admin.ModelAdmin):
    list_display = ('nome','descricao')
    list_display_icons = True
    list_per_page = 10

@admin.register(TipoVarredura)
class TipoVarreduraAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao')
    list_display_icons = True
    list_per_page = 10

@admin.register(SistemaVarredura)
class SistemaVarreduraAdmin(admin.ModelAdmin):
    list_display = ('aplicacao_seguranca','tipo_varredura','usa_webhook','situacao','get_aplicacoes')
    #filter_horizontal = ('get_aplicacoes')
    list_display_icons = True
    list_per_page = 10

@admin.register(Aplicacao)
class AplicacaoAdmin(admin.ModelAdmin):
    list_display = ('nome','sigla', 'descricao',
                    'categoria','url_codigo_fonte',
                    'data_descontinuacao',
                    'tipo_aplicacao','aplicacao_pai','usuario_servico'
                    )
    #filter_horizontal = ('versoes')
    list_display_icons = True
    list_per_page = 5
    
@admin.register(VersaoAplicacao)
class VersaoAplicacaoAdmin(admin.ModelAdmin):
    list_display = ('aplicacao','nome_versao','data_lancamento','descricao','situacao')
    list_display_icons = True
    list_per_page = 10   

@admin.register(ModeloDocumento)    
class ModeloDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao','tipo_modelo','modelo','ativo')
    list_display_icons = True
    list_per_page = 10
    
@admin.register(ArquivoConfiguracao)
class ArquivoConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ('configuracao','descricao','modelo_documento','tipo_arquivo','arquivo')
    list_display_icons = True
    list_per_page = 10
   
@admin.register(Configuracao)
class ConfiguracaoAdmin(admin.ModelAdmin):
     list_display = ('versao_aplicacao','ativo_infraestrutura','descricao', 'ambiente')
     list_display_icons = True
     list_per_page = 10
     
@admin.register(TipoAtivoInfraestrutura)   
class TipoAtivoInfraestruturaAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao')
    list_display_icons = True
    list_per_page = 10

@admin.register(AtivoInfraestrutura)
class AtivoInfraestruturaAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao','tipo_ativo','situacao')
    list_display_icons = True
    list_per_page = 10
    
@admin.register(TipoRelacionamento)
class TipoRelacionamentoAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao')
    list_display_icons = True
    list_per_page = 10

@admin.register(Relacionamento)
class RelacionamentoAdmin(admin.ModelAdmin):
    list_display = ('ativo_infraestrutura','aplicacao','tipo_relacao')
    list_display_icons = True
    list_per_page = 10   

# ativos de infraestrutura    
@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome_servico','protocolo','porta','url','usuario','senha')
                    #'servidor','status')
    #filter_horizontal = ('aplicacoes',)
    list_display_icons = True
    list_per_page = 10

@admin.register(Rede)
class Rede(admin.ModelAdmin):
    list_display = ('tipo','ip','mascara','gateway','ativo_infraestrutura')
    #filter_horizontal = ('servidores',)
    list_display_icons = True
    list_per_page = 10      
    
@admin.register(BancoDados) 
class BancoDados(admin.ModelAdmin):
    list_display = ('nome','tipo','ambiente','versao','string_conexao','ativo_infraestrutura')
    #filter_horizontal = ('aplicacoes',)
    list_display_icons = True
    list_per_page = 10
    
@admin.register(Servidor)
class Servidor(admin.ModelAdmin):
    list_display = ('tipo','sistema_operacional','arquitetura','processador','memoria','disco','get_redes','get_servicos','get_bancos_dados')
    filter_horizontal = ('redes','servicos','bancos_dados')
    list_display_icons = True
    list_per_page = 10

# modelos de documemntos
# @admin.register(TipoModeloDocumento)
# class TipoModeloDocumentoAdmin(admin.ModelAdmin):
#     list_display = ('nome','descricao')
#     list_display_icons = True
#     list_per_page = 10
    
       
