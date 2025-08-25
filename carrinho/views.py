from django.shortcuts import render, redirect
from loja.models import Produto
from .models import Carrinho, CarrinhoItem

# Create your views here.
from django.http import HttpResponse 

def _carrinho_id(request):
    carrinho = request.session.session_key
    if not carrinho:
        carrinho = request.session.create()
    return carrinho

def add_carrinho(request, produto_id):
    produto = Produto.objects.get(id=produto_id)
    try:
        carrinho = Carrinho.objects.get(carrinho_id=_carrinho_id(request))
    except Carrinho.DoesNotExist:
        carrinho = Carrinho.objects.create(
            carrinho_id = _carrinho_id(request)
        )
    carrinho.save()

    try:
        carrinho_item = CarrinhoItem.objects.get(produto=produto, carrinho=carrinho)
        carrinho_item.quantidade += 1
        carrinho_item.save()
    except CarrinhoItem.DoesNotExist:
        carrinho_item = CarrinhoItem.objects.create(
            produto = produto,
            quantidade = 1,
            carrinho = carrinho,
        )
        carrinho_item.save()
    return HttpResponse(carrinho_item.produto)
    exite()
    return redirect('carrinho')

def carrinho(request, total=0, quantidade=0, carrinho_itens=None):
    try:
        carrinho= Carrinho.objects.get(_carrinho_id(request))
        carrinho_itens = CarrinhoItem.objects.filter(carrinho=carrinho, esata_ativo=True)
        for carrinho_item in carrinho_itens:
            total += (carrinho_item.produto.preço * carrinho_item.quantidade)
            quantidade += carrinho_item.quantidade
    except ObjectNotExist:
        pass 
    
    context = {
        'total' :total,
        'quantidade' : quantidade,
        'carrinho_itens' : carrinho_itens,
    }

    return render(request, 'loja/carrinho.html', context)
