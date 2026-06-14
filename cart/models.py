from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Cart(models.Model):
    """Panier d'achat utilisateur"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Panier de {self.user.username}"

    def get_total_price(self):
        """Calcule le prix total du panier"""
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_items(self):
        """Retourne le nombre total d'articles dans le panier"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Article dans le panier"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    def get_total_price(self):
        """Calcule le prix total pour cet article"""
        return self.product.price * self.quantity
