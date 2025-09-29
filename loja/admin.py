from django.contrib import admin
from .models import Produto, Variação, NotaAvaliacao, GaleriaProduto
import admin_thumbnails

# Register your models here.

@admin_thumbnails.thumbnail('imagem')
class GaleriaProdutoInline(admin.TabularInline):
    model = GaleriaProduto
    extra = 1

class ProdutoAdm(admin.ModelAdmin):
    list_display = ('nome_produto', 'preço', 'quantidade', 'categoria', 'data_modificação', 'esta_disponível')
    prepopulated_fields = {'slug': ('nome_produto',)}
    inlines = [GaleriaProdutoInline]


class VariaçãoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'variação_categoria', 'valor_variação', 'esta_ativo')
    list_editable = ('esta_ativo',)
    list_filter = ('produto', 'variação_categoria', 'valor_variação')

admin.site.register(Produto, ProdutoAdm)
admin.site.register(Variação, VariaçãoAdmin)
admin.site.register(NotaAvaliacao)
admin.site.register(GaleriaProduto)