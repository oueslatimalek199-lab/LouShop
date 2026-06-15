from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm


@login_required  # si l'utilisateur n'est pas connecté, Django le redirige
                  # automatiquement vers LOGIN_URL (= "login", voir settings.py)
                  # avec ?next=/commande/commander/ pour revenir ici après connexion
def order_create(request):
    """
    Page de checkout : affiche le formulaire d'adresse + récap du panier.
    À la validation, crée la Order + les OrderItem, vide le panier et
    décrémente le stock.
    """
    cart = Cart(request)

    # On ne peut pas commander un panier vide
    if len(cart) == 0:
        messages.warning(request, "Ton panier est vide.")
        return redirect("cart_detail")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # commit=False : on récupère l'objet Order SANS le sauvegarder
            # tout de suite, pour pouvoir d'abord lui assigner "user"
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # Pour chaque article du panier -> une ligne OrderItem
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )

                # On décrémente le stock du produit
                product = item["product"]
                product.stock = max(product.stock - item["quantity"], 0)
                # Si le stock tombe à 0, on peut aussi le rendre indisponible
                if product.stock == 0:
                    product.available = False
                product.save()

            # La commande est enregistrée -> on vide le panier
            cart.clear()

            return redirect("order_created", order_id=order.id)
    else:
        # Pré-remplit l'email avec celui du compte, pour gagner du temps
        form = OrderCreateForm(initial={"email": request.user.email})

    return render(request, "orders/order_create.html", {"cart": cart, "form": form})


@login_required
def order_created(request, order_id):
    """Page de confirmation après une commande réussie."""
    # On filtre par user=request.user pour qu'un utilisateur ne puisse pas
    # voir la confirmation de la commande de quelqu'un d'autre en changeant
    # juste l'ID dans l'URL.
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_created.html", {"order": order})


@login_required
def order_list(request):
    """Historique des commandes de l'utilisateur connecté."""
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders/order_list.html", {"orders": orders})
