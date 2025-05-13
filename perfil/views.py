from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ServicoForm
from .models import Servico, Comentario, Perfil
from chat.models import Conversation
from django.db.models import Avg

@login_required
def perfil(request):
    # busca o perfil do prestador
    perfil_obj = get_object_or_404(Perfil, user=request.user)

    # formulário pré-populado
    form = ServicoForm(initial={
        'email':    request.user.email,
        'nome':     perfil_obj.nome,
        'contacto': perfil_obj.contacto,
        'distrito': perfil_obj.distrito,
    })

    # anota cada serviço com a média de 'comentarios__classificacao'
    servicos = Servico.objects.filter(prestador=perfil_obj).annotate(
        avg_rating=Avg('comentarios__classificacao')
    )

    return render(request, 'perfil/perfil.html', {
        'perfil':   perfil_obj,
        'form':     form,
        'servicos': servicos,
    })

    # Filtra serviços corretamente com base no User, não no Perfil
    servicos = Servico.objects.filter(prestador=perfil)


    # Calcula a média das classificações
    servicos_com_classificacao = []
    for servico in servicos:
        classificacoes = Classificacao.objects.filter(servico=servico)
        if classificacoes.exists():
            media = sum(c.classificacao for c in classificacoes) / classificacoes.count()
        else:
            media = 0
        servicos_com_classificacao.append((servico, media))

    return render(request, 'perfil/perfil.html', {
        'perfil': perfil,
        'form': form,
        'servicos_com_classificacao': servicos_com_classificacao
    })

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
@csrf_exempt
def adicionar_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                servico = form.save(commit=False)
                perfil = Perfil.objects.get(user=request.user)  # 🔁 Correto: obter o Perfil
                servico.prestador = perfil                     # ✅ Associar corretamente
                servico.save()
                return JsonResponse({'success': True})
            except Perfil.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Perfil não encontrado'}, status=404)
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=500)
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)


@login_required
@csrf_exempt
def editar_servico(request, pk):
    servico = get_object_or_404(Servico, id=pk, prestador__user=request.user)
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
    
