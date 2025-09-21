from django.contrib import admin
from .models import Pagamento, Pedido, ProdutoPedido

# Register your models here.

class ProdutoPedidoInline(admin.TabularInline):
    model = ProdutoPedido
    readonly_fields = ('pagamento', 'usuário', 'produto', 'quantidade', 'preço_produto', 'ordenado')
    extra = 0

class PedidoAdm(admin.ModelAdmin):
    list_display = ['número_pedido', 'nome_completo', 'telefone', 'email', 'cidade', 'total_pedido', 'status', 'é_pedido', 'criado_em']
    list_filter = ['status', 'é_pedido']
    search_fields = ['número_pedido', 'nome', 'sobrenome','telefone', 'email']
    list_per_page = 20
    inlines = [ProdutoPedidoInline]

admin.site.register(Pagamento)
admin.site.register(Pedido, PedidoAdm)
admin.site.register(ProdutoPedido)
