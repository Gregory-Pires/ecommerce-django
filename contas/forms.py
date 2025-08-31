from django import forms
from .models import Conta

class CadastroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Digitar Senha',
        'class': 'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmar Senha'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Digitar Senha',
        'class': 'form-control',
    }))

    class Meta:
        model = Conta
        fields = ['nome', 'sobrenome', 'numero_telefone', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(CadastroForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs['placeholder'] = 'Digite seu Nome'
        self.fields['sobrenome'].widget.attrs['placeholder'] = 'Digite seu Sobrenomeome'
        self.fields['numero_telefone'].widget.attrs['placeholder'] = 'Digite o Número de Telefone'
        self.fields['email'].widget.attrs['placeholder'] = 'Digite seu Email'
        for field in self.fields:    
            self.fields[field].widget.attrs['class'] = 'form-control'