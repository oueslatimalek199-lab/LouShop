from django.urls import path
from . import views

urlpatterns = [
    # Page d'accueil = liste des produits
    # ex: http://127.0.0.1:8000/
    path("", views.home, name="home"),

    # Page détail d'un produit
    # <slug:slug> capture une portion de l'URL (le slug du produit) et
    # la passe à la vue product_detail() en argument "slug"
    # ex: http://127.0.0.1:8000/produit/t-shirt-noir/
    path("produit/<slug:slug>/", views.product_detail, name="product_detail"),
]
