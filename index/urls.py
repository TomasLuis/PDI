from django.urls import path
from . import views

app_name = 'index'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/sugestoes/servicos/', views.obter_sugestoes_servicos, name='sugestoes_servicos'),
    path('pesquisa/', views.resultados_pesquisa, name='resultados_pesquisa'),
    path('servico/<int:servico_id>/', views.detalhes_servico, name='detalhes_servico'), # Adicionada a URL para a página de detalhes
    path('servico/<int:servico_id>/comentar/', views.enviar_comentario, name='enviar_comentario'), # Adicione esta linha
]
