from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Affiche les OrderItem directement DANS la page d'une Order
    (au lieu d'avoir à naviguer dans une liste séparée).
    """
    model = OrderItem
    raw_id_fields = ["product"]
    extra = 0  # pas de ligne vide supplémentaire par défaut


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "email", "user", "city", "paid", "created_at"]
    list_filter = ["paid", "created_at"]
    search_fields = ["full_name", "email"]
    inlines = [OrderItemInline]
