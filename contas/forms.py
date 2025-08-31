from django import forms
from .models import Conta

class CadastroForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ['nome', 'sobrenome', 'numero_telefone', 'email', 'password']