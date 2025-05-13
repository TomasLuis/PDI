"""
URL configuration for skillcraft project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import: from my_app import views
    2. Add a URL to urlpatterns: path('', views.home, name='home')
Class-based views
    1. Add an import: from other_app.views import Home
    2. Add a URL to urlpatterns: path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views # Importe as views de autenticação
from perfil import views
import os
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registo/', include('registo.urls')),
    path('login/', include('login.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='index:index'), name='logout'), # Adicione a URL de logout
    path('', include('index.urls')),
    path('perfil/', views.perfil, name='perfil'),
    path('atualizar_perfil/', views.atualizar_perfil, name='atualizar_perfil'),
    path('adicionar_servico/', views.adicionar_servico, name='adicionar_servico'),
    path('editar_servico/<int:pk>/', views.editar_servico, name='editar_servico'),
    path('atualizar_foto_perfil/', views.atualizar_foto_perfil, name='atualizar_foto_perfil'), # Adicione esta linha
    path('quem_somos/', serve, {'path': 'quem_somos/quem_somos.html', 'document_root': os.path.join(settings.BASE_DIR, 'quem_somos', 'static')}),
    path('chat/', include('chat.urls', namespace='chat')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
