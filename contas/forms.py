from django import forms
from .models import Conta, PerfilUsuario
import re

# ==========================
# Função auxiliar: validação de CPF
# ==========================
def validar_cpf_field(cpf, model=None, instance=None):
    cpf_numbers = ''.join(filter(str.isdigit, str(cpf)))

    if len(cpf_numbers) != 11:
        raise forms.ValidationError("Digite um CPF válido (11 números).")

    if cpf_numbers == cpf_numbers[0] * 11:
        raise forms.ValidationError("CPF inválido.")

    # Verifica duplicidade no banco (exclui o registro atual, se for edição)
    if model and model.objects.filter(cpf=cpf_numbers).exclude(pk=getattr(instance, 'pk', None)).exists():
        raise forms.ValidationError("Este CPF já está cadastrado.")

    # Cálculo dos dígitos verificadores
    def calcula_digito(cpf_slice):
        soma = sum(int(c) * f for c, f in zip(cpf_slice, range(len(cpf_slice)+1, 1, -1)))
        digito = (soma * 10) % 11
        return digito if digito < 10 else 0

    if int(cpf_numbers[9]) != calcula_digito(cpf_numbers[:9]):
        raise forms.ValidationError("CPF inválido.")
    if int(cpf_numbers[10]) != calcula_digito(cpf_numbers[:10]):
        raise forms.ValidationError("CPF inválido.")

    return cpf_numbers


# ==========================
# Formulário de cadastro
# ==========================
class CadastroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
       
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        
    }))
    cpf = forms.CharField(widget=forms.TextInput(attrs={
        'maxlength': '11',
       
    }))
    numero_telefone = forms.CharField(widget=forms.TextInput(attrs={
        'maxlength': '11',
        
    }))

    class Meta:
        model = Conta
        fields = ['nome', 'sobrenome', 'numero_telefone', 'email', 'cpf', 'password']

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        return validar_cpf_field(cpf, model=Conta)

    def clean_numero_telefone(self):
        telefone = self.cleaned_data.get('numero_telefone', '')
        numeros = re.sub(r'\D', '', str(telefone))
        if len(numeros) < 10 or len(numeros) > 11:
            raise forms.ValidationError("Digite um número de telefone válido.")
        return numeros

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("As senhas precisam ser iguais!")


# ==========================
# Formulário de edição de usuário (perfil)
# ==========================
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ('nome', 'sobrenome', 'numero_telefone', 'cpf')

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        return validar_cpf_field(cpf, model=Conta, instance=self.instance)

    def clean_numero_telefone(self):
        telefone = self.cleaned_data.get('numero_telefone', '')
        numeros = re.sub(r'\D', '', str(telefone))
        if len(numeros) < 10 or len(numeros) > 11:
            raise forms.ValidationError("Digite um número de telefone válido.")
        return numeros

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


# ==========================
# Formulário de perfil do usuário
# ==========================
class PerfilUsuarioForm(forms.ModelForm):
    foto_perfil = forms.ImageField(
        required=False,
        error_messages={'invalid': "Apenas arquivos de imagens"},
        widget=forms.FileInput
    )

    class Meta:
        model = PerfilUsuario
        fields = ('estado', 'cidade', 'endereço', 'bairro', 'cep', 'número', 'foto_perfil')

    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        if cep is not None:
            cep = str(cep)
            numeros = re.sub(r'\D', '', cep)
            if len(numeros) != 8:
                raise forms.ValidationError('CEP deve conter 8 dígitos numéricos.')
            return numeros
        return cep

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            # Adicionando placeholders e máscaras
            if field == 'cep':
                self.fields[field].widget.attrs.update({
                    'placeholder': '00000-000'
                })
            if field == 'número':
                self.fields[field].widget.attrs.update({
                    'placeholder': 'Número da residência'
                })
