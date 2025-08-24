from django.shortcuts import render, get_object_or_404
from .models import Produto
from categoria.models import Categoria

# Create your views here.

def loja(request, slug_categoria=None):
    categorias = None
    produtos = None

    if slug_categoria !=None:
        categorias = get_object_or_404(Categoria, slug=slug_categoria)
        produtos = Produto.objects.filter(categoria=categorias, esta_disponível=True)
        contador_produtos = produtos.count()
    else:
        produtos = Produto.objects.all().filter(esta_disponível=True)
        contador_produtos = produtos.count()

    context = {
        'produtos': produtos,
        'contador_produtos': contador_produtos,
    }
    return render(request, 'loja/loja.html', context)