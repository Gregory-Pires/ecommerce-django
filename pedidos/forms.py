from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nome', 'sobrenome', 'telefone', 'email', 'rua', 'número', 'cidade', 'estado', 'nota_pedido']