from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login

def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Faz login automático após o registro
            return redirect("index")  # Redireciona para a página inicial
    else:
        form = SignUpForm()

    return render(request, "registo/registarUtilizador.html", {"form": form})
