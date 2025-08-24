from django.db import models

# Create your models here.

class Categoria(models.Model):
    nome_categria = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    descrição = models.TextField(max_length=255, blank=True)
    imagem_cat = models.ImageField(upload_to='photos/categorias', blank=True)

    def __str__(self):
        return self.nome_categria