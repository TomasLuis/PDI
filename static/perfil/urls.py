from django.urls import path
from . import views

urlpatterns = [
    path('', views.perfil, name='perfil'),
    path('atualizar/', views.atualizar_perfil, name='atualizar_perfil'), # Escolha esta ou a próxima linha
    # path('atualizar_perfil/', views.atualizar_perfil, name='atualizar_perfil'), # Remova esta linha
    path('adicionar_servico/', views.adicionar_servico, name='adicionar_servico'),
    path('editar_servico/<int:servico_id>/', views.editar_servico, name='editar_servico'),
    # path('atualizar_dados/', views.alterar_dados, name='alterar_dados'), # Remova esta linha
    path('apagar_servico/<int:servico_id>/', views.apagar_servico, name='apagar_servico'),
    path('atualizar_foto_perfil/', views.atualizar_foto_perfil, name='atualizar_foto_perfil'),
    
] 