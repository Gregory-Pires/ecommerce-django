from django.contrib import admin
from .models import Pagamento, Pedido, ProdutoPedido

# Register your models here.

admin.site.register(Pagamento)
admin.site.register(Pedido)
admin.site.register(ProdutoPedido)
