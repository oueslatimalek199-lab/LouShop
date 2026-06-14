from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    fieldsets = (
        ('Informations', {'fields': ('name', 'description', 'category')}),
        ('Pricing & Stock', {'fields': ('price', 'stock')}),
        ('Médias', {'fields': ('image',)}),
        ('Status', {'fields': ('is_active',)}),
    )
