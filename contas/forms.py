from django import forms
from .models import Conta, PerfilUsuario
import re

class CadastroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Digitar Senha',
        'class': 'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmar Senha',
        'class': 'form-control',
    }))

    cpf = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '000.000.000-00',
        'maxlength': '14',   # limite de caracteres já formatado
        'class': 'form-control',
    }))

    numero_telefone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '(00) 00000-0000',
        'maxlength': '15',
        'class': 'form-control',
    }))

    class Meta:
        model = Conta
        fields = ['nome', 'sobrenome', 'numero_telefone', 'email', 'cpf', 'password']

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        # Remove pontos e traço
        cpf_numbers = ''.join(filter(str.isdigit, cpf))

        if len(cpf_numbers) != 11:
            raise forms.ValidationError("Digite um CPF válido (11 números).")

        # Verifica se todos os números são iguais
        if cpf_numbers == cpf_numbers[0] * 11:
            raise forms.ValidationError("CPF inválido.")

        # Verifica se já existe no banco
        if Conta.objects.filter(cpf=cpf_numbers).exists():
            raise forms.ValidationError("Este CPF já está cadastrado.")

        # Função para calcular dígito verificador
        def calcula_digito(cpf_slice):
            soma = sum(int(c) * f for c, f in zip(cpf_slice, range(len(cpf_slice)+1, 1, -1)))
            digito = (soma * 10) % 11
            return digito if digito < 10 else 0

        # Validação dos dígitos
        if int(cpf_numbers[9]) != calcula_digito(cpf_numbers[:9]):
            raise forms.ValidationError("CPF inválido.")
        if int(cpf_numbers[10]) != calcula_digito(cpf_numbers[:10]):
            raise forms.ValidationError("CPF inválido.")

        return cpf_numbers
    
    def clean_numero_telefone(self):
        telefone = self.cleaned_data['numero_telefone']
        # Remove qualquer caractere que não seja número
        numeros = re.sub(r'\D', '', telefone)
        
        if len(numeros) < 10 or len(numeros) > 11:
            raise forms.ValidationError("Digite um número de telefone válido.")
        
        return numeros
        
    def clean(self):
        cleaned_data = super(CadastroForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                  "As senhas precisam ser iguais!"
            )        

    def __init__(self, *args, **kwargs):
        super(CadastroForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs['placeholder'] = 'Digite seu Nome'
        self.fields['sobrenome'].widget.attrs['placeholder'] = 'Digite seu Sobrenome'        
        self.fields['email'].widget.attrs['placeholder'] = 'Digite seu Email'
        for field in self.fields:    
            self.fields[field].widget.attrs['class'] = 'form-control'

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ('nome', 'sobrenome', 'numero_telefone', 'cpf')
    
    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        for field in self.fields:    
            self.fields[field].widget.attrs['class'] = 'form-control'

class PerfilUsuarioForm(forms.ModelForm):
    foto_perfil = forms.ImageField(required=False, error_messages = {'inválido':{"Apenas arquivos de imagens"}}, widget=forms.FileInput)
    class Meta:
        model = PerfilUsuario
        fields = ('estado', 'cidade', 'rua', 'número', 'foto_perfil')
    
    def __init__(self, *args, **kwargs):
        super(PerfilUsuarioForm, self).__init__(*args, **kwargs)
        for field in self.fields:    
            self.fields[field].widget.attrs['class'] = 'form-control'



        