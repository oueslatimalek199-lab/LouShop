from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ["id", "full_name", "email", "city", "status", "paid", "created_at"]
    list_filter   = ["status", "paid", "created_at"]
    search_fields = ["full_name", "email"]

    # Permet de changer status et paid directement depuis la liste,
    # sans ouvrir chaque commande
    list_editable = ["status", "paid"]

    inlines = [OrderItemInline]

    # Action en masse : marquer plusieurs commandes comme "Livrées" en 1 clic
    actions = ["mark_delivered"]

    @admin.action(description="Marquer les commandes sélectionnées comme Livrées")
    def mark_delivered(self, request, queryset):
        updated = queryset.update(status=Order.STATUS_DELIVERED, paid=True)
        self.message_user(request, f"{updated} commande(s) marquée(s) comme livrée(s).")
