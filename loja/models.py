from django.db import models
from categoria.models import Categoria
from django.urls import reverse
# Create your models here.

class Produto(models.Model):
    nome_produto     = models.CharField(max_length=200, unique=True)
    slug             = models.SlugField(max_length=200, unique=True)
    descrição        = models.TextField(max_length=500, blank=True)
    preço            = models.FloatField()
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