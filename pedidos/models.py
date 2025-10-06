from django.db import models
from contas.models import Conta
from loja.models import Produto, Variação

# Create your models here.

class Pagamento(models.Model):
    usuário = models.ForeignKey(Conta, on_delete=models.CASCADE)
    pagamento_id = models.CharField(max_length=100)
    metodo_pagamento = models.CharField(max_length=100)
    quantia_paga = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pagamento_id
    
class Pedido(models.Model):
    STATUS = (
        ('Novo', 'Novo'),
        ('Aceito', 'Aceito'),
        ('Completo', 'Completo'),
        ('Cancelado', 'Cancelado'),
    )

    usuário = models.ForeignKey(Conta, on_delete=models.SET_NULL, null=True)
    pagamento = models.ForeignKey(Pagamento, on_delete=models.SET_NULL, blank=True, null=True)
    número_pedido = models.CharField(max_length=20)
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    endereço = models.CharField(max_length=50)    
    número = models.IntegerField()
    bairro = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    cep = models.IntegerField()
    nota_pedido = models.CharField(max_length=100, blank=True)
    total_pedido = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='Novo')
    ip = models.CharField(blank=True,  max_length=20)
    é_pedido = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def nome_completo(self):
        return f'{self.nome} {self.sobrenome}'

    def endereço_completo(self):
        return f'{self.endereço}, {self.número}'
    
    def __str__(self):
        return self.nome
    
class ProdutoPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    pagamento = models.ForeignKey(Pagamento, on_delete=models.SET_NULL, blank=True, null=True)
    usuário = models.ForeignKey(Conta, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    variações = models.ManyToManyField(Variação, blank=True)
    quantidade = models.IntegerField()
    preço_produto = models.FloatField()
    ordenado = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.produto.nome_produto   

