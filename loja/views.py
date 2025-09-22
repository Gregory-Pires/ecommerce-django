from django.shortcuts import render, get_object_or_404, redirect
from .models import Produto, NotaAvaliacao
from categoria.models import Categoria
from carrinhos.models import CarrinhoItem
from django.db.models import Q

from carrinhos.views import _carrinho_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.http import HttpResponse
from .forms import ReviewForm
from django.contrib import messages
from pedidos.models import ProdutoPedido
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
    
    if request.user.is_authenticated:
        try:
            produtopedido = ProdutoPedido.objects.filter(usuário=request.user, produto_id=produto_unico.id).exists()
        except ProdutoPedido.DoesNotExist:
            produtopedido = None
    else:
        produtopedido = None
    
    avaliacoes = NotaAvaliacao.objects.filter(produto_id=produto_unico.id, status=True)

    context = {
        'produto_unico': produto_unico,
        'in_carrinho': in_carrinho,
        'produtopedido': produtopedido,
        'avaliacoes': avaliacoes,
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

def enviar_avaliacao(request, produto_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            avaliacoes = NotaAvaliacao.objects.get(usuário__id=request.user.id, produto__id=produto_id)
            form = ReviewForm(request.POST, instance=avaliacoes)
            form.save()
            messages.success(request, 'Muito obrigado! sua avaliação foi atualizada.')
            return redirect(url)
        except NotaAvaliacao.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = NotaAvaliacao()
                data.assunto = form.cleaned_data['assunto']
                data.nota = form.cleaned_data['nota']
                data.avaliação = form.cleaned_data['avaliação']
                data.ip = request.META.get('REMOTE_ADDR')
                data.produto_id = produto_id
                data.usuário_id = request.user.id
                data.save()
                messages.success(request, 'Muito obrigado! sua avaliação foi enviada.')
                return redirect(url)
