from django.contrib import admin
from .models import Especialista
from perfil.models import Comentario

# Registra o modelo para aparecer no painel de administração
admin.site.register(Especialista)
admin.site.register(Comentario)