from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def home(request):
    """
    Page d'accueil : affiche la liste de tous les produits disponibles.

    On peut filtrer par catégorie via l'URL, ex: /?categorie=chaussures
    """
    # On ne récupère que les produits "available=True"
    products = Product.objects.filter(available=True)

    # request.GET contient les paramètres de l'URL après le "?"
    # ex: /?categorie=chaussures -> request.GET.get("categorie") = "chaussures"
    category_slug = request.GET.get("categorie")
    selected_category = None

    if category_slug:
        # get_object_or_404 : récupère l'objet, ou affiche une page 404
        # si rien ne correspond (évite un crash brutal du serveur)
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    # On récupère aussi toutes les catégories pour afficher un menu de filtre
    categories = Category.objects.all()

    # "context" = dictionnaire des variables qu'on envoie au template HTML
    context = {
        "products": products,
        "categories": categories,
        "selected_category": selected_category,
    }
    return render(request, "products/home.html", context)


def product_detail(request, slug):
    """
    Page détail d'un produit, identifié par son "slug" dans l'URL
    (ex: /produit/t-shirt-noir/).
    """
    # On cherche le produit correspondant au slug, parmi les produits
    # disponibles. Si aucun ne correspond -> page 404 automatique.
    product = get_object_or_404(Product, slug=slug, available=True)

    context = {
        "product": product,
    }
    return render(request, "products/product_detail.html", context)
