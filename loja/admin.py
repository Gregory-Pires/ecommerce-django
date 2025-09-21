from django.contrib import admin
from .models import Produto, Variação, NotaAvaliacao

# Register your models here.

class ProdutoAdm(admin.ModelAdmin):
    list_display = ('nome_produto', 'preço', 'quantidade', 'categoria', 'data_modificação', 'esta_disponível')
    prepopulated_fields = {'slug': ('nome_produto',)}

class VariaçãoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'variação_categoria', 'valor_variação', 'esta_ativo')
    list_editable = ('esta_ativo',)
    list_filter = ('produto', 'variação_categoria', 'valor_variação')

admin.site.register(Produto, ProdutoAdm)
admin.site.register(Variação, VariaçãoAdmin)
admin.site.register(NotaAvaliacao)