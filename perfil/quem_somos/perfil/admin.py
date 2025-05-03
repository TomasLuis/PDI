from django.contrib import admin
from .models import Perfil, Servico

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'nome', 'contacto', 'distrito')
    search_fields = ('user__username', 'nome', 'contacto', 'distrito')

admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Servico) 