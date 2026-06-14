from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Informations', {'fields': ('order_number', 'user', 'status')}),
        ('Adresse de livraison', {
            'fields': ('address', 'city', 'zip_code', 'country', 'phone_number')
        }),
        ('Montants', {'fields': ('subtotal', 'shipping_cost', 'total_amount')}),
        ('Dates', {'fields': ('created_at', 'updated_at', 'shipped_at', 'delivered_at')}),
    )
