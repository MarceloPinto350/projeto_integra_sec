from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.models import User, Group
from .models import Categoria, Abrangencia, AreaNegocial, Sistema


class CustomAdminSite(admin.AdminSite):
    site_header = 'Sistema de Apoio a DevSecOps - SYSDSO'
    site_title = 'Sistema de Apoio a DevSecOps - SYSDSO'
    index_title = 'Bem-vindo ao SYSDSO'

admin.site = CustomAdminSite()

class CategoriaAdmin(ModelAdmin):
    list_display = ('descricao', 'ativa')
    list_display_icons = True
    list_per_page = 10
admin.site.register(Categoria, CategoriaAdmin)

class AbrangenciaAdmin(ModelAdmin):
    list_display = ('descricao','ativa')
    list_display_icons = True
    list_per_page = 10
admin.site.register(Abrangencia, AbrangenciaAdmin)

class AreaNegocialAdmin(ModelAdmin):
    list_display = ('descricao','sigla','identificador_sigep','ativa')
    list_display_icons = True
    list_per_page = 10
admin.site.register(AreaNegocial, AreaNegocialAdmin)  
    
class SistemaAdmin(ModelAdmin):
    list_display = ('nome','sigla','descricao','categoria','abrangencia','url_fonte','area_responsavel','gestor_negocial','data_registro','data_atualizacao','data_descontinuacao')
    list_display_icons = True
    list_per_page = 10   
    readonly_fields = ('data_registro','data_atualizacao') 
admin.site.register(Sistema, SistemaAdmin)   

    
