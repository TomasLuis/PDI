from django.shortcuts import render, get_object_or_404, redirect
from index.models import Especialista, Servico  # Importe o modelo Servico
from perfil.models import Servico, Comentario  # Importe o model Comentario do perfil
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse  # Importe HttpResponse
from django.db.models import Q, Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import Round
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def pesquisar_especialistas(request):
    especialistas = Especialista.objects.order_by('-classificacao')[:4]  # Pega os 4 melhores especialistas
    return render(request, 'index/index.html', {'especialistas': especialistas})


# Retorna sugestões para a pesquisa inteligente (SERVIÇOS)
def obter_sugestoes_servicos(request):
    query = request.GET.get('q', '')
    if query:
        servicos = Servico.objects.filter(categoria__icontains=query).values('categoria').distinct()[:10]
        return JsonResponse([{"categoria_servico": s['categoria']} for s in servicos], safe=False)
    return JsonResponse([], safe=False)


# Exibe os resultados da pesquisa
def resultados_pesquisa(request):
    query = request.GET.get('q', '')
    order_by = request.GET.get('order_by', '')
    distrito = request.GET.get('distrito', '')  # Alterado de localidade para distrito

    resultados = Servico.objects.all()

    if query:
        resultados = resultados.filter(
            Q(nome__icontains=query) |
            Q(categoria__icontains=query) |
            Q(informacoes_adicionais__icontains=query)
        )

    if distrito:  # Alterado de localidade para distrito
        resultados = resultados.filter(distrito=distrito)  # Alterado de localidade para distrito

    if order_by == 'melhores_classificados':
        resultados = resultados.annotate(avg_avaliacao=Round(Avg('avaliacao'), 1)).order_by(
            '-avg_avaliacao', 'nome')
    elif order_by == 'nome':
        resultados = resultados.order_by('nome')

    distritos = Servico.objects.values_list('distrito', flat=True).distinct().order_by(
        'distrito')  # Alterado de localidade para distrito

    paginator = Paginator(resultados, 6)
    page = request.GET.get('page')

    try:
        resultados_pagina = paginator.page(page)
    except PageNotAnInteger:
        resultados_pagina = paginator.page(1)
    except EmptyPage:
        resultados_pagina = paginator.page(paginator.num_pages)

    context = {
        'resultados_pagina': resultados_pagina,
        'query': query,
        'total_resultados': resultados.count(),
        'num_paginas': paginator.num_pages,
        'pagina_atual': resultados_pagina.number,
        'range_paginas': range(1, paginator.num_pages + 1),
        'distritos': distritos,  # Alterado de distritos para distritos
        'order_by': order_by,
        'distrito_selecionado': distrito,  # Alterado de localidade_selecionada para distrito_selecionado
    }
    return render(request, 'index/resultados.html', context)


def detalhes_servico(request, servico_id):
    servico = get_object_or_404(Servico, pk=servico_id)
    comentarios = Comentario.objects.filter(servico=servico).order_by('-data_criacao')

    # Calcula a média das classificações
    media_classificacao = comentarios.aggregate(Avg('classificacao'))['classificacao__avg'] or 0

    context = {
        'servico': servico,
        'comentarios': comentarios,
        'media_classificacao': round(media_classificacao, 1),  # Arredonda para uma casa decimal
    }
    return render(request, 'index/detalhes_servico.html', context)


@login_required
def enviar_comentario(request, servico_id):
    servico = get_object_or_404(Servico, pk=servico_id)
    if request.method == 'POST':
        comentario_texto = request.POST.get('comentario')
        classificacao = request.POST.get('classificacao')  # Captura a classificação do formulário

        nome_utilizador = request.user.username

        # Cria o comentário com a classificação
        comentario = Comentario(
            servico=servico,
            nome_utilizador=nome_utilizador,
            comentario=comentario_texto,
            classificacao=classificacao
        )
        comentario.save()
        return redirect('index:detalhes_servico', servico_id=servico_id)

    return redirect(reverse('index:detalhes_servico', kwargs={'servico_id': servico.id}))
