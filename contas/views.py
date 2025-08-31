from django.shortcuts import render
from .forms import CadastroForm

# Create your views here.

def cadastro(request):
    form = CadastroForm()
    context = {
        'form': form,
    }
    return render(request, 'contas/cadastro.html', context)

def login(request):
    return render(request, 'contas/login.html')

def logout(request):
    return

