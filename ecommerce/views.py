from django.shortcuts import render
from loja.models import Produto

def home(request):
    produtos = Produto.objects.all().filter(esta_disponível=True)

    context = {
        'produtos': produtos,
    }
    return render(request, 'home.html', context)