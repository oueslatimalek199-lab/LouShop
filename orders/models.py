from django.conf import settings
from django.db import models
from products.models import Product


class Order(models.Model):
    """
    Une commande passée par un utilisateur.

    On stocke les infos de livraison directement ici (full_name, email,
    address, city) plutôt que d'aller les chercher sur le User : ça permet
    de garder une "photo" de l'adresse au moment de la commande, même si
    l'utilisateur change son profil plus tard.
    """

    # settings.AUTH_USER_MODEL = 'auth.User' (le modèle User par défaut de Django)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="orders",
        on_delete=models.CASCADE,
    )

    full_name = models.CharField("Nom complet", max_length=150)
    email = models.EmailField("Email")
    address = models.CharField("Adresse", max_length=250)
    city = models.CharField("Ville", max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    # On pourrait brancher un vrai paiement plus tard ; pour l'instant
    # ce champ permet juste de marquer une commande comme "traitée".
    paid = models.BooleanField("Payée", default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Commande #{self.id}"

    def get_total_cost(self):
        """Somme des sous-totaux de chaque ligne de la commande."""
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """
    Une ligne de commande : un produit, sa quantité, et son prix
    AU MOMENT DE LA COMMANDE (important : si le prix du produit change
    plus tard, l'historique de la commande ne doit pas changer).
    """

    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.CASCADE)

    price = models.DecimalField("Prix unitaire", max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField("Quantité", default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        """Sous-total de cette ligne (prix x quantité)."""
        return self.price * self.quantity
