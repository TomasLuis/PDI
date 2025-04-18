from django.shortcuts import render
from index.models import Especialista  # Importe o modelo Servico
from perfil.models import Servico
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import Round

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
    distrito = request.GET.get('distrito', '') # Alterado de localidade para distrito

    resultados = Servico.objects.all()

    if query:
        resultados = resultados.filter(
            Q(nome__icontains=query) |
            Q(categoria__icontains=query) |
            Q(informacoes_adicionais__icontains=query)
        )

    if distrito: # Alterado de localidade para distrito
        resultados = resultados.filter(distrito=distrito) # Alterado de localidade para distrito

    if order_by == 'melhores_classificados':
        resultados = resultados.annotate(avg_avaliacao=Round(Avg('avaliacao'), 1)).order_by('-avg_avaliacao', 'nome')
    elif order_by == 'nome':
        resultados = resultados.order_by('nome')

    distritos = Servico.objects.values_list('distrito', flat=True).distinct().order_by('distrito') # Alterado de localidade para distrito

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
        'distritos': distritos, # Alterado de distritos para distritos
        'order_by': order_by,
        'distrito_selecionado': distrito, # Alterado de localidade_selecionada para distrito_selecionado
    }
    return render(request, 'resultados.html', context)
