from django.shortcuts import render
from .models import Produto

# Create your views here.

def loja(request):
    produtos = Produto.objects.all().filter(esta_disponível=True)
    contador_produtos = produtos.count()

    context = {
        'produtos': produtos,
        'contador_produtos': contador_produtos,
    }
    return render(request, 'loja/loja.html', context)