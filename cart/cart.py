"""
Logique du panier, basée sur la SESSION Django.

Pourquoi la session et pas un modèle (table BDD) ?
-> Comme on n'a pas encore l'inscription/connexion (étape suivante),
   on veut que le panier fonctionne même pour un visiteur non connecté.
   La session permet de stocker des données propres à chaque visiteur,
   côté serveur, sans avoir besoin d'un compte.

Le panier est stocké comme un dictionnaire dans la session, par exemple :
{
    "3": {"quantity": 2, "price": "29.90"},
    "7": {"quantity": 1, "price": "149.00"},
}
où "3" et "7" sont les IDs des produits (Product.id).
"""

from decimal import Decimal
from django.conf import settings
from products.models import Product


class Cart:
    def __init__(self, request):
        # On récupère la session de la requête (Django gère ça automatiquement
        # via un cookie côté navigateur)
        self.session = request.session

        # On essaie de récupérer un panier existant dans la session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # Pas encore de panier -> on en crée un vide
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Ajoute un produit au panier, ou met à jour sa quantité.
        """
        product_id = str(product.id)  # les clés de session doivent être des strings

        if product_id not in self.cart:
            # Première fois qu'on ajoute ce produit -> on initialise
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}

        if update_quantity:
            # update_quantity=True -> on REMPLACE la quantité (depuis la page panier)
            self.cart[product_id]["quantity"] = quantity
        else:
            # update_quantity=False -> on AJOUTE à la quantité existante
            # (depuis la page produit, clic sur "Ajouter au panier")
            self.cart[product_id]["quantity"] += quantity

        self.save()

    def save(self):
        # Indique à Django que la session a été modifiée, pour qu'il
        # la sauvegarde (sinon les changements dans un dict imbriqué
        # ne sont pas détectés automatiquement)
        self.session.modified = True

    def remove(self, product):
        """Supprime complètement un produit du panier."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Permet de faire "for item in cart" (utilisé dans le template).
        Pour chaque produit du panier, on va chercher l'objet Product
        correspondant en BDD, et on calcule le sous-total.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        # On travaille sur une copie pour ne pas modifier self.cart directement
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            # Decimal = type précis pour l'argent (évite les erreurs d'arrondi)
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Permet de faire "len(cart)" ou "{{ cart|length }}" dans un template.
        Renvoie le nombre TOTAL d'articles (en comptant les quantités).
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """Renvoie le prix total du panier."""
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def clear(self):
        """Vide complètement le panier (utilisé après une commande validée)."""
        del self.session[settings.CART_SESSION_ID]
        self.save()
