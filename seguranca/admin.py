from django.contrib import admin
from .models import (TipoAplicacao, AreaNegocial, Aplicacao, VersaoAplicacao, 
    #TipoAtivoInfraestrutura, AtivoInfraestrutura, 
    TipoVarredura,SistemaVarredura, Servico, Servidor,Rede,BancoDados,
    TipoModeloDocumento,ModeloDocumento
    )

#class CustomAdminSite(admin.AdminSite):
#    site_header = 'Sistema de integração de segurança de aplicações - SISAP'
#    site_title = 'Sistema de integração de segurança de aplicações - SISAP'
#    index_title = 'Bem-vindo ao SISAP'
#admin.site = CustomAdminSite()

@admin.register(TipoAplicacao)
class TipoAplicacaoAdmin (admin.ModelAdmin):
    list_display = ('nome','descricao')
    list_display_icons = True
    list_per_page = 10

@admin.register(AreaNegocial)
class AreaNegocialAdmin (admin.ModelAdmin):
    list_display = ('nome','sigla','id_sigep','ativa')
    list_display_icons = True
    list_per_page = 10

@admin.register(Aplicacao)
class AplicacaoAdmin(admin.ModelAdmin):
    list_display = ('nome','sigla', #'descricao',
                    'categoria','url_fonte',
                    #'data_registro','data_atualizacao',
                    'data_descontinuacao',
                    #'area_analista_liberacao','abrangencia','area_responsavel','gestor_negocial',
                    #'essencial','estrategico','arquitetura','hospedagem',
                    'tipo','url_acesso','aplicacao_pai','usuario_servico'
                    #,'senha_servico','token_acesso'                 
                    )
    #filter_horizontal = ('versoes')
    list_display_icons = True
    list_per_page = 5
    
@admin.register(VersaoAplicacao)
class VersaoAplicacaoAdmin(admin.ModelAdmin):
    list_display = ('aplicacao','nome_versao','data_lancamento','descricao','situacao')
    list_display_icons = True
    list_per_page = 10   

# @admin.register(TipoAtivoInfraestrutura)
# class TipoAtivoInfraestruturaAdmin(admin.ModelAdmin):
#     list_display = ('nome','descricao')
#     list_display_icons = True
#     list_per_page = 10
    
# @admin.register(AtivoInfraestrutura)
# class AtivoInfraestruturaAdmin(admin.ModelAdmin):
#     list_display = ('nome','descricao','tipo','url_localizacao','endereco_ip','porta_acesso',
#                     'usuario_acesso',
#                     #'senha_acesso','token_acesso',
#                     'status')
#     list_display_icons = True
#     list_per_page = 10
    
@admin.register(TipoVarredura)
class TipoVarreduraAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao')
    list_display_icons = True
    list_per_page = 10
    
@admin.register(SistemaVarredura)
class SistemaVarreduraAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao','url','usuario','status')
    list_display_icons = True
    list_per_page = 10

# ativos de infraestrutura    
@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao','protocolo','url','usuario','senha','servidor','status')
    filter_horizontal = ('aplicacoes',)
    list_display_icons = True
    list_per_page = 10

@admin.register(Servidor)
class Servidor(admin.ModelAdmin):
    list_display = ('nome','descricao','tipo','ip','sistema_operacional','processador','memoria','disco','status')
    filter_horizontal = ('servicos','aplicacoes')
    list_display_icons = True
    list_per_page = 10

@admin.register(Rede)
class Rede(admin.ModelAdmin):
    list_display = ('nome','descricao','tipo','ip','mascara','gateway','dns_primario','dns_secundario','status')
    filter_horizontal = ('servidores',)
    list_display_icons = True
    list_per_page = 10      
    
@admin.register(BancoDados) 
class BancoDados(admin.ModelAdmin):
    list_display = ('nome','descricao','tipo','ip','porta','usuario','senha','servidor','status')
    filter_horizontal = ('aplicacoes',)
    list_display_icons = True
    list_per_page = 10
    
# modelos de documemntos
@admin.register(TipoModeloDocumento)
class TipoModeloDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao')
    list_display_icons = True
    list_per_page = 10
    
@admin.register(ModeloDocumento)    
class ModeloDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao','tipo','arquivo','ativa')
    list_display_icons = True
    list_per_page = 10
    
       
