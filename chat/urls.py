from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('<int:conversation_id>/', views.chat_room, name='chat_room'),
    path('iniciar/<int:servico_id>/', views.iniciar_conversa, name='iniciar_conversa'),
    path('conversas/', views.chat_list, name='chat_list'),
    path('minhas-conversas/', views.minhas_conversas, name='minhas_conversas'),
]
