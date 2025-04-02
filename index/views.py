from django.shortcuts import render
from index.models import Especialista

def pesquisar_especialistas(request):
    especialistas = Especialista.objects.order_by('-classificacao')[:4]  # Pega os 4 melhores especialistas
    return render(request, 'index/index.html', {'especialistas': especialistas})
