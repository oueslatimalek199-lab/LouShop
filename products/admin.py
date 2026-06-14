from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Personnalise l'affichage de Category dans /admin/.
    """
    # Colonnes affichées dans la liste des catégories
    list_display = ["name", "slug"]

    # Remplit automatiquement le champ "slug" à partir du champ "name"
    # quand on tape dans le formulaire admin (ex: "Vêtements" -> "vetements")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Personnalise l'affichage de Product dans /admin/.
    """
    # Colonnes visibles dans la liste des produits
    list_display = ["name", "category", "price", "stock", "available", "created_at"]

    # Permet de filtrer la liste sur le côté droit de l'admin
    list_filter = ["available", "category"]

    # Ajoute une barre de recherche (par nom de produit)
    search_fields = ["name", "description"]

    # Permet de modifier "available" directement depuis la liste,
    # sans ouvrir chaque produit
    list_editable = ["available", "stock"]

    # Remplit automatiquement le slug à partir du nom
    prepopulated_fields = {"slug": ("name",)}
