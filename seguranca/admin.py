from django.contrib import admin
from .models import TipoAplicacao, AreaNegocial, Aplicacao, VersaoAplicacao, TipoAtivoInfraestrutura, AtivoInfraestrutura, TipoVarredura,SistemaVarredura

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
    list_display = ('nome','sigla','descricao','categoria','url_fonte',
                    'data_registro','data_atualizacao','data_descontinuacao',
                    #'area_analista_liberacao','abrangencia','area_responsavel','gestor_negocial',
                    #'essencial','estrategico','arquitetura','hospedagem',
                    'tipo','url_acesso','aplicacao_pai',
                    'usuario_servico','senha_servico','token_acesso'                 
                    )
    list_display_icons = True
    list_per_page = 5
    
@admin.register(VersaoAplicacao)
class VersaoAplicacaoAdmin(admin.ModelAdmin):
    list_display = ('aplicacao','nome_versao','data_lancamento','descricao','situacao')
    list_display_icons = True
    list_per_page = 10   

@admin.register(TipoAtivoInfraestrutura)
class TipoAtivoInfraestruturaAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao')
    list_display_icons = True
    list_per_page = 10
    
@admin.register(AtivoInfraestrutura)
class AtivoInfraestruturaAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao','tipo','url_localizacao','endereco_ip','porta_acesso',
                    'usuario_acesso','senha_acesso','token_acesso','status')
    list_display_icons = True
    list_per_page = 10
    
@admin.register(TipoVarredura)
class TipoVarreduraAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao')
    list_display_icons = True
    list_per_page = 10
    
@admin.register(SistemaVarredura)
class SistemaVarreduraAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao','tipo','url','usuario','senha','token','status')
    list_display_icons = True
    list_per_page = 10