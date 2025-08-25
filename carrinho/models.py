from django.db import models
from loja.models import Produto

# Create your models here.

class Carrinho(models.Model):
    carrinho_id = models.CharField(max_length=250, blank=True)
    data_criação = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.carrinho_id
    
class CarrinhoItem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    esta_ativo = models.BooleanField(default=True)

    def sub_total(self):
        return self.produto.preço * self.quantidade

    def __str__(self):
        return self.produto
