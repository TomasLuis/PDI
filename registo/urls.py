from django.urls import path
from .views import register

urlpatterns = [
    path("registarUtilizador/", register, name="registar"),
]
