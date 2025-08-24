from django.contrib import admin
from .models import Produto

# Register your models here.

class ProdutoAdm(admin.ModelAdmin):
    list_display = ('nome_produto', 'preço', 'quantidade', 'categoria', 'data_modificação', 'esta_disponível')
    prepopulated_fields = {'slug': ('nome_produto',)}

admin.site.register(Produto, ProdutoAdm)