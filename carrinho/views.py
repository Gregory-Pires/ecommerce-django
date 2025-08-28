from django.shortcuts import render, redirect, get_object_or_404
from loja.models import Produto, Variação
from .models import Carrinho, CarrinhoItem
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse
# Create your views here.

def _carrinho_id(request):
    carrinho = request.session.session_key
    if not carrinho:
        carrinho = request.session.create()
    return carrinho

def add_carrinho(request, produto_id):
    produto = Produto.objects.get(id=produto_id)
    variação_produto = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            
            try:
                variação = Variação.objects.get(produto=produto, variação_categoria__iexact=key, valor_variação__iexact=value)
                variação_produto.append(variaçãoa)
            except:
                pass

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
    return redirect('carrinho')

def remover_carrinho(request, produto_id):
    carrinho = Carrinho.objects.get(carrinho_id=_carrinho_id(request))
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho_item = CarrinhoItem.objects.get(produto=produto, carrinho=carrinho)
    if carrinho_item.quantidade > 1:
        carrinho_item.quantidade -= 1
        carrinho_item.save()
    else:
        carrinho_item.delete()
    return redirect('carrinho')

def remover_carrinho_item(request, produto_id):
    carrinho = Carrinho.objects.get(carrinho_id=_carrinho_id(request))
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho_item = CarrinhoItem.objects.get(produto=produto, carrinho=carrinho)
    carrinho_item.delete()
    return redirect('carrinho')

def carrinho(request, total=0, quantidade=0, carrinho_itens=None):
    try:
        carrinho= Carrinho.objects.get(carrinho_id=_carrinho_id(request))
        carrinho_itens = CarrinhoItem.objects.filter(carrinho=carrinho, esta_ativo=True)
        for carrinho_item in carrinho_itens:
            total += (carrinho_item.produto.preço * carrinho_item.quantidade)
            quantidade += carrinho_item.quantidade
    except ObjectDoesNotExist:
        pass 
    
    context = {
        'total' :total,
        'quantidade' : quantidade,
        'carrinho_itens' : carrinho_itens,
    }

    return render(request, 'loja/carrinho.html', context)
