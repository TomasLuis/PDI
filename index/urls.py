from django.urls import path
from . import views

urlpatterns = [
    path('', views.pesquisar_especialistas, name='index'),
    path('api/sugestoes/servicos/', views.obter_sugestoes_servicos, name='sugestoes_servicos'),
    path('pesquisa/', views.resultados_pesquisa, name='resultados_pesquisa'),
]