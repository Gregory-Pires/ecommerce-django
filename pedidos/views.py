from django.shortcuts import render, redirect
from django.http import HttpResponse
from carrinhos.models import CarrinhoItem
from .forms import PedidoForm
import datetime
from .models import Pedido, Pagamento, ProdutoPedido
import json
from loja.models import Produto

# Create your views here.

def pagamentos(request):
    body = json.loads(request.body)
    pedido = Pedido.objects.get(usuário=request.user, é_pedido=False, número_pedido=body['orderID'])
    
    pagamento = Pagamento(
        usuário = request.user,
        pagamento_id = body['transID'],
        metodo_pagamento = body['payment_method'],
        quantia_paga = pedido.total_pedido,
        status = body['status'],
    )
    pagamento.save()

    pedido.pagamento = pagamento
    pedido.é_pedido = True
    pedido.save()

    carrinho_itens = CarrinhoItem.objects.filter(usuário=request.user)

    for item in carrinho_itens:
        produtopedido = ProdutoPedido()
        produtopedido.pedido_id = pedido.id
        produtopedido.pagamento = pagamento
        produtopedido.usuário_id = item.usuário.id
        produtopedido.produto_id = item.produto_id
        produtopedido.quantidade = item.quantidade
        produtopedido.preço_produto = item.produto.preço
        produtopedido.ordenado = True
        produtopedido.save()

        carrinho_item = CarrinhoItem.objects.get(id=item.id)
        variação_produto = carrinho_item.variações.all()
        produtopedido = ProdutoPedido.objects.get(id=produtopedido.id)
        produtopedido.variações.set(variação_produto)
        produtopedido.save

    
        produto = Produto.objects.get(id=item.produto_id)
        produto.quantidade -= item.quantidade
        produto.save()

    CarrinhoItem.objects.filter(usuário=request.user).delete()

    
    return render(request, 'pedidos/pagamentos.html')

def fazer_pedido(request, total=0, quantidade=0):
    current_user = request.user


    carrinho_itens = CarrinhoItem.objects.filter(usuário=current_user)
    carrinho_contador = carrinho_itens.count()
    if carrinho_contador <=0:
        return redirect('loja')
    
    for carrinho_item in carrinho_itens:
        total += (carrinho_item.produto.preço * carrinho_item.quantidade)
        quantidade += carrinho_item.quantidade

    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            data = Pedido()
            data.usuário = current_user
            data.nome = form.cleaned_data['nome']           
            data.sobrenome = form.cleaned_data['sobrenome'] 
            data.telefone = form.cleaned_data['telefone'] 
            data.email = form.cleaned_data['email'] 
            data.rua = form.cleaned_data['rua'] 
            data.número = form.cleaned_data['número'] 
            data.estado = form.cleaned_data['estado'] 
            data.cidade = form.cleaned_data['cidade'] 
            data.nota_pedido = form.cleaned_data['nota_pedido'] 
            data.total_pedido = total 
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            #Gerando número do pedido
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt) 
            current_date = d.strftime("%d%m%Y")
            número_pedido = current_date + str(data.id)
            data.número_pedido = número_pedido
            data.save()

            pedido = Pedido.objects.get(usuário=current_user, é_pedido=False, número_pedido=número_pedido)
            context = {
                'pedido': pedido,
                'carrinho_itens': carrinho_itens,
                'total': total,
            }
            return render(request, 'pedidos/pagamentos.html', context)
    else:
        return redirect('checkout')