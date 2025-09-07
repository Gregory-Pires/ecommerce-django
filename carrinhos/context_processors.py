from .models import Carrinho, CarrinhoItem
from .views import _carrinho_id

def contador(request):
    carrinho_contador = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            carrinho = Carrinho.objects.filter(carrinho_id=_carrinho_id(request))
            carrinho_itens = CarrinhoItem.objects.all().filter(carrinho=carrinho[:1])
            for carrinho_item in carrinho_itens:
                carrinho_contador += carrinho_item.quantidade
        except Carrinho.DoesNotExist:
            carrinho_contador = 0
    return dict(carrinho_contador=carrinho_contador)