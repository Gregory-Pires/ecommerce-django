from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nome', 'sobrenome', 'telefone', 'email', 'endereço_1', 'endereço_2', 'cidade', 'estado', 'nota_pedido']