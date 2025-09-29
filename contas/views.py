
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CadastroForm, UsuarioForm, PerfilUsuarioForm
from .models import Conta, PerfilUsuario
from pedidos.models import Pedido, ProdutoPedido
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

from carrinhos.views import _carrinho_id
from carrinhos.models import Carrinho, CarrinhoItem
import requests

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

            #Cria Perfil de Usuário
            perfil = PerfilUsuario()
            perfil.usuário_id = user.id
            perfil.foto_perfil = 'padrao/usuario-padrao.jpg'
            perfil.save()

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
            return redirect('/conta/login/?command=ativacao&email='+email)
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
            try:
                carrinho = Carrinho.objects.get(carrinho_id=_carrinho_id(request))
                carrinho_item_existe = CarrinhoItem.objects.filter(carrinho=carrinho).exists()

                if carrinho_item_existe:
                    carrinho_items_sessao = CarrinhoItem.objects.filter(carrinho=carrinho)

                    # 🔹 variações do carrinho da sessão
                    variacoes_sessao = []
                    for item in carrinho_items_sessao:
                        variacoes_sessao.append(set(item.variações.all()))  # já vira set

                    # 🔹 variações do carrinho do usuário
                    carrinho_items_user = CarrinhoItem.objects.filter(usuário=user)
                    ex_var_list = []
                    id_list = []
                    for item in carrinho_items_user:
                        ex_var_list.append(set(item.variações.all()))
                        id_list.append(item.id)

                    # 🔹 compara sets e une carrinhos
                    for pr in variacoes_sessao:
                        if pr in ex_var_list:
                            # se já existe, aumenta a quantidade
                            index = ex_var_list.index(pr)
                            item_id = id_list[index]
                            item = CarrinhoItem.objects.get(id=item_id)
                            item.quantidade += 1
                            item.usuário = user
                            item.save()
                        else:
                            # se não existe, só transfere o item de sessão para o usuário
                            for item in carrinho_items_sessao:
                                item.usuário = user
                                item.carrinho = None  # desvincula do carrinho da sessão
                                item.save()
            except Carrinho.DoesNotExist:
                pass

            auth.login(request, user)
            messages.success(request, 'Você entrou com sucesso!')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)                
            except:
                return redirect('painel')
        else:
            messages.error(request, 'Credenciais incorretas.')
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
    pedidos = Pedido.objects.order_by('criado_em').filter(usuário_id=request.user.id, é_pedido=True)
    pedidos_contador = pedidos.count()
    context = {
        'pedidos_contador': pedidos_contador,
    }
    return render(request, 'contas/painel.html', context)

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

def resetsenha_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Conta._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Conta.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Por favor crie uma nova senha')
        return redirect('resetsenha')
    else:
        messages.error(request, 'Esse link expirou!')
        return redirect('login')
    
def resetsenha(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Conta.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Senha mudada com sucesso')
            return redirect('login')
        else:
            messages.error(request, 'As senha precisam ser iguais!')
            return redirect('resetsenha')
    else:
        return render(request, 'contas/resetsenha.html')
    

@login_required(login_url='login')
def meus_pedidos(request):
    pedidos = Pedido.objects.filter(usuário=request.user, é_pedido=True).order_by('-criado_em')
    context = {
        'pedidos': pedidos,
    }
    return render(request, 'contas/meus_pedidos.html', context)

@login_required(login_url='login')
def editar_perfil(request):
    perfilusuario = get_object_or_404(PerfilUsuario, usuário=request.user)
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST, instance=request.user)
        perfil_form = PerfilUsuarioForm(request.POST, request.FILES, instance=perfilusuario)
        if usuario_form.is_valid() and perfil_form.is_valid():
            usuario_form.save()
            perfil_form.save()
            messages.success(request, 'Seu perfil foi atualizado.')
            return redirect('editar_perfil')
    else:
        usuario_form = UsuarioForm(instance=request.user)
        perfil_form = PerfilUsuarioForm(instance=perfilusuario)
    context = {
        'usuario_form': usuario_form,
        'perfil_form': perfil_form,
        'perfilusuario': perfilusuario,
    }
    return render(request, 'contas/editar_perfil.html', context)

@login_required(login_url='login')
def mudar_senha(request):
    if request.method == 'POST':
        senha_atual = request.POST['senha_atual']
        senha_nova = request.POST['senha_nova']
        confirmar_senha = request.POST['confirmar_senha']

        usuario = Conta.objects.get(nome_usuário__exact=request.user.nome_usuário)

        if senha_nova == confirmar_senha:
            success = usuario.check_password(senha_atual)
            if success:
                usuario.set_password(senha_nova)
                usuario.save()
                #auth.logout(request)
                messages.success(request, 'Senha atualizada com sucesso.')
                return redirect('mudar_senha')
            else:
                messages.error(request, 'Por favor digite a senha atual correta')
                return redirect('mudar_senha')
        else:
            messages.error(request, 'As senhas não coincidem!')
            return redirect('mudar_senha')

    return render(request, 'contas/mudar_senha.html')


@login_required(login_url='login')
def detalhes_pedido(request, pedido_id):
    detalhes_pedido = ProdutoPedido.objects.filter(pedido__número_pedido=pedido_id)
    pedido = Pedido.objects.get(número_pedido=pedido_id)
    total = 0
    total_item = 0

    for i in detalhes_pedido:
        total += i.preço_produto * i.quantidade

    for item in detalhes_pedido:
        item.total_item = item.preço_produto * item.quantidade

    context = {
        'detalhes_pedido': detalhes_pedido,
        'pedido': pedido,
        'total': total,
        'total_item': total_item,
    }
    return render(request, 'contas/detalhes_pedido.html', context)