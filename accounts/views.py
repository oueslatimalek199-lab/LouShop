from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegisterForm


def register(request):
    """
    Page d'inscription.

    GET  -> affiche le formulaire vide
    POST -> valide le formulaire, crée l'utilisateur, le connecte
            automatiquement, puis redirige vers l'accueil
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # form.save() crée l'utilisateur en BDD (mot de passe déjà
            # "hashé" automatiquement par UserCreationForm, jamais stocké en clair)
            user = form.save()

            # On connecte directement le nouvel utilisateur
            login(request, user)

            # messages.success() ajoute un message "flash" affiché une seule fois
            # (voir {% if messages %} dans base.html)
            messages.success(request, f"Bienvenue {user.username} ! Ton compte a été créé.")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})
