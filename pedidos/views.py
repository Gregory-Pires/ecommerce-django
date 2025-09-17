from django.shortcuts import render, redirect
from django.http import HttpResponse
from carrinhos.models import CarrinhoItem
from .forms import PedidoForm
import datetime
from .models import Pedido

# Create your views here.

def pagamentos(request):
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
            data.endereço_1 = form.cleaned_data['endereço_1'] 
            data.endereço_2 = form.cleaned_data['endereço_2'] 
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
            return redirect('checkout')
    else:
        return redirect('checkout')