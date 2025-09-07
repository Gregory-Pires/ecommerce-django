
from django.shortcuts import render, redirect
from .forms import CadastroForm
from .models import Conta
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.

#verificação email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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

            #USER actvation
            current_site = get_current_site(request)
            mail_subject = 'Por favor ative sua conta'
            message = render_to_string('contas/verificação_conta_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            #messages.success(request, 'Muito obrigado por se cadastrar conosco. Enviamos um email para a ativação da conta. Por favor verifique seu email')
            return redirect('/contas/login/?command=ativacao&email='+email)
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
            messages.success(request, 'Você Entrou.')
            return redirect('painel')
        else:
            messages.error(request, 'Credencias erradas')
            return redirect('login')
    return render(request, 'contas/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,  'Você saiu.')
    return redirect('login')

def ativar(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Conta._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Conta.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Parabéns! sua conta foi ativada. ')
        return redirect('login')
    else:
        messages.error(request, 'Link de validação inválido')
        return redirect('cadastro')

@login_required(login_url = 'login')
def painel(request):
    return render(request, 'contas/painel.html')

def esqueceusuasenha(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Conta.objects.filter(email=email).exists():
            user = Conta.objects.get(email__exact=email)
            
            #Email para resetar senha
            current_site = get_current_site(request)
            mail_subject = 'Por favor crie uma nova senha'
            message = render_to_string('contas/reset_senha_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'A criação de uma nova senha foi enviada para o seu email.')
            return redirect('login')        
        else:
            messages.error(request, 'Essa conta não existe!')
            return redirect('esqueceusuasenha')

    return render(request, 'contas/esqueceusuasenha.html')

def resetsenha_validate(request):
    return HttpResponse('ok')