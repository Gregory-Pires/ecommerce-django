from django.shortcuts import render, get_object_or_404
from .models import Produto
from categoria.models import Categoria
from carrinhos.models import CarrinhoItem
from django.db.models import Q

from carrinhos.views import _carrinho_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.http import HttpResponse
# Create your views here.

def loja(request, slug_categoria=None):
    categorias = None
    produtos = None

    if slug_categoria !=None:
        categorias = get_object_or_404(Categoria, slug=slug_categoria)
        produtos = Produto.objects.filter(categoria=categorias, esta_disponível=True)
        paginator = Paginator(produtos, 3)
        page = request.GET.get('page')
        paged_produtos = paginator.get_page(page)
        contador_produtos = produtos.count()
    else:
        produtos = Produto.objects.all().filter(esta_disponível=True).order_by('id')
        paginator = Paginator(produtos, 3)
        page = request.GET.get('page')
        paged_produtos = paginator.get_page(page)
        contador_produtos = produtos.count()

    context = {
        'produtos': paged_produtos,
        'contador_produtos': contador_produtos,
    }
    return render(request, 'loja/loja.html', context)

def produto_detail(request, slug_categoria, slug_produto):
    try:
        produto_unico = Produto.objects.get(categoria__slug=slug_categoria, slug=slug_produto)
        in_carrinho = CarrinhoItem.objects.filter(carrinho__carrinho_id=_carrinho_id(request), produto=produto_unico).exists()
    except Exception as e:
        raise e
    context = {
        'produto_unico': produto_unico,
        'in_carrinho': in_carrinho
    }
    return render(request, 'loja/produto_detail.html', context)

def pesquisa(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            produtos = Produto.objects.order_by('-data_criação').filter(Q(descrição__icontains=keyword) | Q(nome_produto__icontains=keyword))
            contador_produtos = produtos.count()
    context = {
        'produtos': produtos,
        'contador_produtos': contador_produtos,
    }
    return render(request, 'loja/loja.html', context)