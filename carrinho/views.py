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
                variação_produto.append(variação)
            except:
                pass

    try:
        carrinho = Carrinho.objects.get(carrinho_id=_carrinho_id(request))
    except Carrinho.DoesNotExist:
        carrinho = Carrinho.objects.create(
            carrinho_id = _carrinho_id(request)
        )
    carrinho.save()

    carrinho_item_existe = CarrinhoItem.objects.filter(produto=produto, carrinho=carrinho).exists()
    if carrinho_item_existe:   
        carrinho_item = CarrinhoItem.objects.filter(produto=produto, carrinho=carrinho)

        ex_var_list = []
        id = []
        for item in carrinho_item:
            variacao_existente = item.variações.all()
            ex_var_list.append(list(variacao_existente))
            id.append(item.id)

        print(ex_var_list)

        if variação_produto in ex_var_list:
            index = ex_var_list.index(variação_produto)
            item_id = id[index]
            item = CarrinhoItem.objects.get(produto=produto, id=item_id)
            item.quantidade +=1
            item.save()

            
        else:
            item = CarrinhoItem.objects.create(produto=produto, quantidade=1, carrinho=carrinho)     
            if len(variação_produto) > 0:
                item.variações.clear()
                item.variações.add(*variação_produto)
            item.save()
    else:        
        carrinho_item = CarrinhoItem.objects.create(
            produto = produto,
            quantidade = 1,
            carrinho = carrinho,
        )
        if len(variação_produto) > 0:
            carrinho_item.variações.clear()
            carrinho_item.variações.add(*variação_produto)
        carrinho_item.save()   
    return redirect('carrinho')

def remover_carrinho(request, produto_id, carrinho_item_id):
    carrinho = Carrinho.objects.get(carrinho_id=_carrinho_id(request))
    produto = get_object_or_404(Produto, id=produto_id)
    try:
        carrinho_item = CarrinhoItem.objects.get(produto=produto, carrinho=carrinho, id=carrinho_item_id)
        if carrinho_item.quantidade > 1:
            carrinho_item.quantidade -= 1
            carrinho_item.save()
        else:
            carrinho_item.delete()
    except:
        pass
    return redirect('carrinho')

def remover_carrinho_item(request, produto_id, carrinho_item_id):
    carrinho = Carrinho.objects.get(carrinho_id=_carrinho_id(request))
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho_item = CarrinhoItem.objects.get(produto=produto, carrinho=carrinho, id=carrinho_item_id)
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
