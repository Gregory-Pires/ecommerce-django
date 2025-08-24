from django.db import models
from django.urls import reverse

# Create your models here.

class Categoria(models.Model):
    nome_categoria = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    descrição = models.TextField(max_length=255, blank=True)
    imagem_cat = models.ImageField(upload_to='photos/categorias', blank=True)

    def get_url(self):
        return reverse('produtos_por_categoria', args=[self.slug])
    
    def __str__(self):
        return self.nome_categoria