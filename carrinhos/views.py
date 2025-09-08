from django.shortcuts import render, redirect, get_object_or_404
from loja.models import Produto, Variação
from .models import Carrinho, CarrinhoItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
# Create your views here.

def _carrinho_id(request):
    carrinho = request.session.session_key
    if not carrinho:
        carrinho = request.session.create()
    return carrinho

def add_carrinho(request, produto_id):
    current_user = request.user
    produto = Produto.objects.get(id=produto_id)

    # Função auxiliar para extrair as variações do POST
    def get_variacoes_from_post(produto, request):
        variacoes = []
        if request.method == 'POST':
            for key, value in request.POST.items():
                try:
                    variacao = Variação.objects.get(
                        produto=produto,
                        variação_categoria__iexact=key,
                        valor_variação__iexact=value
                    )
                    variacoes.append(variacao)
                except:
                    pass
        return variacoes

    # 🔹 Usuário logado
    if current_user.is_authenticated:
        variacoes_produto = get_variacoes_from_post(produto, request)

        carrinho_item_existe = CarrinhoItem.objects.filter(produto=produto, usuário=current_user).exists()
        if carrinho_item_existe:
            carrinho_items = CarrinhoItem.objects.filter(produto=produto, usuário=current_user)

            ex_var_list = []
            id_list = []
            for item in carrinho_items:
                variacoes_existentes = item.variações.all()
                ex_var_list.append(set(variacoes_existentes))  # set para evitar problema de ordem
                id_list.append(item.id)

            if set(variacoes_produto) in ex_var_list:
                # Aumenta quantidade do item existente
                index = ex_var_list.index(set(variacoes_produto))
                item_id = id_list[index]
                item = CarrinhoItem.objects.get(produto=produto, id=item_id)
                item.quantidade += 1
                item.save()
            else:
                # Cria novo item de carrinho
                item = CarrinhoItem.objects.create(produto=produto, quantidade=1, usuário=current_user)
                if variacoes_produto:
                    item.variações.add(*variacoes_produto)
                item.save()
        else:
            carrinho_item = CarrinhoItem.objects.create(
                produto=produto,
                quantidade=1,
                usuário=current_user,
            )
            if variacoes_produto:
                carrinho_item.variações.add(*variacoes_produto)
            carrinho_item.save()
        return redirect('carrinho')

    # 🔹 Usuário não logado
    else:
        variacoes_produto = get_variacoes_from_post(produto, request)

        try:
            carrinho = Carrinho.objects.get(carrinho_id=_carrinho_id(request))
        except Carrinho.DoesNotExist:
            carrinho = Carrinho.objects.create(
                carrinho_id=_carrinho_id(request)
            )
        carrinho.save()

        carrinho_item_existe = CarrinhoItem.objects.filter(produto=produto, carrinho=carrinho).exists()
        if carrinho_item_existe:
            carrinho_items = CarrinhoItem.objects.filter(produto=produto, carrinho=carrinho)

            ex_var_list = []
            id_list = []
            for item in carrinho_items:
                variacoes_existentes = item.variações.all()
                ex_var_list.append(set(variacoes_existentes))  # set resolve ordem
                id_list.append(item.id)

            if set(variacoes_produto) in ex_var_list:
                index = ex_var_list.index(set(variacoes_produto))
                item_id = id_list[index]
                item = CarrinhoItem.objects.get(produto=produto, id=item_id)
                item.quantidade += 1
                item.save()
            else:
                item = CarrinhoItem.objects.create(produto=produto, quantidade=1, carrinho=carrinho)
                if variacoes_produto:
                    item.variações.add(*variacoes_produto)
                item.save()
        else:
            carrinho_item = CarrinhoItem.objects.create(
                produto=produto,
                quantidade=1,
                carrinho=carrinho,
            )
            if variacoes_produto:
                carrinho_item.variações.add(*variacoes_produto)
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
        if request.user.is_authenticated:
              carrinho_itens = CarrinhoItem.objects.filter(usuário=request.user, esta_ativo=True)
        else:
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

@login_required(login_url='login')
def checkout(request, total=0, quantidade=0, carrinho_itens=None):
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
    return render(request, 'loja/checkout.html', context)
