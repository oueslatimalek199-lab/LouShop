from django.shortcuts import render


def home(request):
    """Page d'accueil — affichera la liste des produits (étape 2)."""
    return render(request, "products/home.html")
