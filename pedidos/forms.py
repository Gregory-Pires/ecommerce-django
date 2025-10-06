from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nome', 'sobrenome', 'telefone', 'email', 'endereço', 'número', 'bairro', 'cidade', 'cep', 'estado', 'nota_pedido']