
from django.shortcuts import render, redirect
from .forms import CadastroForm
from .models import Conta
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

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
            messages.success(request, 'Cadastro concluído com sucesso')
            return redirect('cadastro')
    else:       
        form = CadastroForm()
    context = {
        'form': form,
    }
    return render(request, 'contas/cadastro.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            #messages.success(request, 'Você Entrou.')
            return redirect('home')
        else:
            messages.error(request, 'Credencias erradas')
            return redirect('login')
    return render(request, 'contas/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,  'Você saiu.')
    return redirect('login')


