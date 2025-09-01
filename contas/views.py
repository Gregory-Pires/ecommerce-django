
from django.shortcuts import render
from .forms import CadastroForm
from .models import Conta
from django.contrib import messages

# Create your views here.

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            sobrenome = form.cleaned_data['sobrenome']
            numero_telefone = form.cleaned_data['numero_telefone']
            email = form.cleaned_data['email']
            cpf = form.cleaned_data['cpf']
            password = form.cleaned_data['password']
            nome_usuário = email.split("@")[0]

            user = Conta.objects.create_user(nome=nome, sobrenome=sobrenome, email=email, numero_telefone=numero_telefone, cpf=cpf, nome_usuário=nome_usuário, password=password )
            user.save()
    else:       
        form = CadastroForm()
    context = {
        'form': form,
    }
    return render(request, 'contas/cadastro.html', context)

def login(request):
    return render(request, 'contas/login.html')

def logout(request):
    return


