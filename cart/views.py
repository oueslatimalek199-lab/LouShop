from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST  # cette vue n'accepte QUE les requêtes POST (sécurité : pas de
               # modification du panier juste en visitant une URL)
def cart_add(request, product_id):
    """
    Ajoute un produit au panier (ou met à jour sa quantité).
    Appelée depuis le formulaire de la page détail produit ou de la page panier.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    # On valide les données envoyées par le formulaire (quantité, update)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data  # cd = "cleaned data", dictionnaire des valeurs validées
        cart.add(
            product=product,
            quantity=cd["quantity"],
            update_quantity=cd["update"],
        )

    # redirect() renvoie l'utilisateur vers une autre page (évite de soumettre
    # le formulaire deux fois si on rafraîchit la page)
    return redirect("cart_detail")


@require_POST
def cart_remove(request, product_id):
    """Retire complètement un produit du panier."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart_detail")


def cart_detail(request):
    """Affiche le contenu du panier."""
    cart = Cart(request)

    # Pour chaque article du panier, on prépare un formulaire pré-rempli
    # avec la quantité actuelle, et "update=True" (pour que la soumission
    # remplace la quantité au lieu de l'additionner)
    for item in cart:
        item["update_quantity_form"] = CartAddProductForm(
            initial={"quantity": item["quantity"], "update": True}
        )

    return render(request, "cart/cart_detail.html", {"cart": cart})
