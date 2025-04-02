from django.urls import path
from .views import pesquisar_especialistas

urlpatterns = [
    path('',pesquisar_especialistas , name='index'),
]