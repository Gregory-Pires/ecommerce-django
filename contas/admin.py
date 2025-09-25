from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Conta, PerfilUsuario
from django.utils.html import format_html

# Register your models here.
class ContaAdm(UserAdmin):
    list_display = ('email', 'nome', 'sobrenome', 'nome_usuário', 'ultimo_login', 'data_cadastro', 'is_active')
    ordering = ('email',)
    list_display_links = ('email', 'nome', 'sobrenome')
    readonly_fields = ('ultimo_login', 'data_cadastro')
    ordering = ('-data_cadastro',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class PerfilUsuarioAdm(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.foto_perfil.url))
    thumbnail.short_description = 'Foto de Perfil'
    list_display = ('thumbnail', 'usuário', 'cidade', 'estado')

admin.site.register(Conta, ContaAdm)
admin.site.register(PerfilUsuario, PerfilUsuarioAdm)