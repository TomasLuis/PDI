from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ServicoForm
from .models import Servico, Classificacao, Perfil

@login_required
def perfil(request):
    perfil = request.user.perfil
    form = ServicoForm(initial={
        'email': request.user.email,
        'nome': request.user.perfil.nome,
        'contacto': request.user.perfil.contacto,
        'distrito': request.user.perfil.distrito,
    })

    servicos_com_classificacao = []
    servicos = Servico.objects.filter(prestador=request.user)
    for servico in servicos:
        classificacoes = Classificacao.objects.filter(servico=servico)
        if classificacoes:
            media_classificacao = sum(c.classificacao for c in classificacoes) / len(classificacoes)
        else:
            media_classificacao = 0
        servicos_com_classificacao.append((servico, media_classificacao))

    return render(request, 'perfil.html', {'perfil': perfil, 'form': form, 'servicos_com_classificacao': servicos_com_classificacao})

@login_required
def atualizar_perfil(request):
    if request.method == 'POST':
        perfil = request.user.perfil
        novo_email = request.POST.get('email')
        nome = request.POST.get('nome')
        contacto = request.POST.get('contacto')
        distrito = request.POST.get('distrito')

        if novo_email and novo_email != request.user.email:
            if User.objects.filter(email=novo_email).exists():
                return render(request, 'perfil.html', {'perfil': perfil, 'erro_email': 'Este email já está em uso.'})
            else:
                request.user.email = novo_email
                request.user.username = novo_email
                request.user.save()
                perfil.user = request.user

        if nome:
            perfil.nome = nome
        if contacto:
            perfil.contacto = contacto
        if distrito:
            perfil.distrito = distrito

        perfil.save()
        return redirect('perfil')
    else:
        return redirect('perfil')

@login_required
def adicionar_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST, request.FILES)
        if form.is_valid():
            servico = form.save(commit=False)
            servico.prestador = request.user  # Garante que o prestador seja atribuído
            servico.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = ServicoForm()
        return render(request, 'perfil.html', {'form': form})

@login_required
@csrf_exempt
def editar_servico(request, pk):
    servico = get_object_or_404(Servico, id=pk, prestador=request.user)
    if request.method == 'POST':
        form = ServicoForm(request.POST, request.FILES, instance=servico)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = ServicoForm(instance=servico)
        form_html = str(form.as_p())  # Renderiza o formulário como parágrafos
        return JsonResponse({'form_html': form_html})
    
@login_required
def apagar_servico(request, servico_id):
    if request.method == 'DELETE':
        servico = get_object_or_404(Servico, id=servico_id, perfil__user=request.user)
        servico.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Método inválido'})
    
@login_required
def atualizar_foto_perfil(request):
    if request.method == 'POST' and request.FILES['foto']:
        foto = request.FILES['foto']
        perfil = Perfil.objects.filter(user=request.user).first()
        if perfil:
            perfil.foto_perfil = foto
            perfil.save()
            # Adiciona a URL da foto à resposta
            return JsonResponse({'success': True, 'foto_url': perfil.foto_perfil.url})
        else:
            return JsonResponse({'success': False, 'error': 'Perfil não encontrado'})
    else:
        return JsonResponse({'success': False, 'error': 'Nenhuma foto enviada'})