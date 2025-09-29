from django.db import models
from categoria.models import Categoria
from django.urls import reverse
from contas.models import Conta
from django.db.models import Avg, Count
# Create your models here.

class Produto(models.Model):
    nome_produto     = models.CharField(max_length=200, unique=True)
    slug             = models.SlugField(max_length=200, unique=True)
    descrição        = models.TextField(max_length=500, blank=True)
    preço            = models.DecimalField(max_digits=10, decimal_places=2)
    imagens          = models.ImageField(upload_to='photos/products')
    quantidade       = models.IntegerField()
    esta_disponível  = models.BooleanField(default=True)
    categoria        = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    data_criação     = models.DateTimeField(auto_now_add=True)
    data_modificação = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('produto_detail', args=(self.categoria.slug, self.slug))
    
    def __str__(self):
        return self.nome_produto
    def notaMedia(self):
        notas = NotaAvaliacao.objects.filter(produto=self, status=True).aggregate(average=Avg('nota'))
        avg = 0
        if notas['average'] is not None:
            avg = float(notas['average'])
        return avg
    
    def countAvaliacao(self):
        notas = NotaAvaliacao.objects.filter(produto=self, status=True).aggregate(count=Count('id'))
        count = 0
        if notas['count'] is not None:
            count = int(notas['count'])
        return count


class VariationManager(models.Manager):
    def cores(self):
        return super(VariationManager, self).filter(variação_categoria='cor', esta_ativo=True)
    
    def tamanhos(self):
        return super(VariationManager, self).filter(variação_categoria='tamanho', esta_ativo=True)

variação_escolha_categoria = (
        ('cor', 'cor'),
        ('tamanho', 'tamanho'),
)
    
class Variação(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    variação_categoria = models.CharField(max_length=100, choices=variação_escolha_categoria)
    valor_variação = models.CharField(max_length=100)
    esta_ativo = models.BooleanField(default=True)
    data_criação = models.DateTimeField(auto_now=True)

    objects = VariationManager()
   
    def __str__(self):
        return self.valor_variação
    
class NotaAvaliacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    usuário = models.ForeignKey(Conta, on_delete=models.CASCADE)
    assunto = models.CharField(max_length=100, blank=True)
    avaliação = models.TextField(max_length=500, blank=True)
    nota = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.assunto 

class GaleriaProduto(models.Model):
    produto = models.ForeignKey(Produto, default=None, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='loja/produtos', max_length=255)

    def __str__(self):
        return self.produto.nome_produto   
    
