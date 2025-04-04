from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.core.mail import send_mail
from django.conf import settings
import random
import time
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_active:  # Adicione esta verificação
                    login(request, user)
                    return redirect('index')
                else:
                    form.add_error(None, 'Usuário inativo.')
            else:
                form.add_error(None, 'Email ou senha incorretos.')
    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})




@csrf_protect
def recuperar_senha_email(request):
    agora = time.time()
    ultimo_envio = request.session.get('ultimo_envio')

    # Limite de 1 minuto entre os envios
    if ultimo_envio and agora - ultimo_envio < 60:
        return render(request, 'login/recuperar_senha_email.html', {'erro': 'Aguarde antes de solicitar outro código.'})

    if request.method == 'POST':
        email = request.POST.get('email')
        codigo = str(random.randint(100000, 999999))  # Gera um código aleatório de 6 dígitos

        # Enviar email com o código
        enviado = send_mail(
            'Código de Recuperação de Senha',
            f'Seu código de recuperação é: {codigo}',
            settings.EMAIL_HOST_USER,  # Configurado no settings.py
            [email],
            fail_silently=False,
        )

        # Lidar com erros de envio de emails
        if enviado == 0:
            return render(request, 'login/recuperar_senha_email.html', {'erro': 'Erro ao enviar email. Tente novamente mais tarde.'})

        # Armazenar o código em sessão com tempo de expiração (3 minutos)
        request.session['codigo_recuperacao'] = codigo
        request.session['email_recuperacao'] = email
        request.session['expiracao_codigo'] = agora + 180  # 180 segundos = 3 minutos
        request.session['ultimo_envio'] = agora

        return redirect('recuperar_senha_codigo')  # Redireciona para a próxima view

    return render(request, 'login/recuperar_senha_email.html')


def recuperar_senha_codigo(request):
    if request.method == 'POST':
        codigo_inserido = ''.join([request.POST.get(f'codigo{i}') for i in range(1, 7)])
        codigo_esperado = request.session.get('codigo_recuperacao')
        email_recuperacao = request.session.get('email_recuperacao')
        expiracao_codigo = request.session.get('expiracao_codigo')

        if codigo_inserido == codigo_esperado and expiracao_codigo and expiracao_codigo > time.time():
            return redirect('nova_passe', email=email_recuperacao)
        else:
            return render(request, 'login/recuperar_senha_codigo.html', {'erro': 'Código inválido ou expirado.'})

    return render(request, 'login/recuperar_senha_codigo.html')

def nova_passe(request, email):
    if request.method == 'POST':
        nova_passe = request.POST.get('nova_passe')
        confirmar_passe = request.POST.get('confirmar_passe')

        if nova_passe == confirmar_passe:
            utilizador = User.objects.get(email=email)
            utilizador.set_password(nova_passe)
            utilizador.save()
            return redirect('login')
        else:
            return render(request, 'login/nova_passe.html', {'erro': 'As passes não coincidem.', 'email': email})

    return render(request, 'login/nova_passe.html', {'email': email})