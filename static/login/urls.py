from django.urls import path
from . import views
from .views import login_view

urlpatterns = [
    path('', login_view, name='login'),
    path('recuperar-senha/email/', views.recuperar_senha_email, name='recuperar_senha_email'),
    path('recuperar-senha/codigo/', views.recuperar_senha_codigo, name='recuperar_senha_codigo'),
    path('nova-passe/<str:email>/', views.nova_passe, name='nova_passe'),
]