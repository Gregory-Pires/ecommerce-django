from django.contrib import admin
from .models import Carrinho, CarrinhoItem


class CarrinhoAdm(admin.ModelAdmin):
    list_display = ('carrinho_id', 'data_criação')

class CarrinhoItemAdm(admin.ModelAdmin):
    list_display = ('produto', 'carrinho', 'quantidade', 'esta_ativo')

admin.site.register(Carrinho, CarrinhoAdm)
admin.site.register(CarrinhoItem, CarrinhoItemAdm)

# Register your models here.
