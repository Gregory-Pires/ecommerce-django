from django.db import models
from categoria.models import Categoria
# Create your models here.

class Produto(models.Model):
    nome_produto     = models.CharField(max_length=200, unique=True)
    slug             = models.SlugField(max_length=200, unique=True)
    descrição        = models.TextField(max_length=500, blank=True)
    preço            = models.IntegerField()
    imagens          = models.ImageField(upload_to='photos/products')
    quantidade       = models.IntegerField()
    esta_disponível  = models.BooleanField(default=True)
    categoria        = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    data_criação     = models.DateTimeField(auto_now_add=True)
    data_modificação = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome_produto