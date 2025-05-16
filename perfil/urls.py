from django.urls import path
from . import views

urlpatterns = [
    path('', views.perfil, name='perfil'),
    path('atualizar/', views.atualizar_perfil, name='atualizar_perfil'),
    path('adicionar_servico/', views.adicionar_servico, name='adicionar_servico'),
    path('editar_servico/<int:servico_id>/', views.editar_servico, name='editar_servico'),
    path('apagar_servico/<int:servico_id>/', views.apagar_servico, name='apagar_servico'),
    path('atualizar_foto_perfil/', views.atualizar_foto_perfil, name='atualizar_foto_perfil'),
    
    
] 