from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Conta

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

admin.site.register(Conta, ContaAdm)