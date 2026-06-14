"""
Commande personnalisée Django.

On peut l'exécuter avec :
    python manage.py seed_products

Elle crée quelques catégories et produits de test, pour ne pas avoir
à tout taper à la main dans l'admin.

(Toute commande Django doit définir une classe "Command" héritant de
BaseCommand, avec une méthode handle().)
"""

from django.core.management.base import BaseCommand
from products.models import Category, Product


class Command(BaseCommand):
    help = "Ajoute des catégories et produits de démonstration"

    def handle(self, *args, **options):
        # --- Catégories ---
        # get_or_create() : récupère l'objet s'il existe déjà (selon "slug"),
        # sinon le crée avec les valeurs de "defaults". Ça évite les doublons
        # si on lance la commande plusieurs fois.
        vetements, _ = Category.objects.get_or_create(
            slug="vetements", defaults={"name": "Vêtements"}
        )
        electronique, _ = Category.objects.get_or_create(
            slug="electronique", defaults={"name": "Électronique"}
        )
        maison, _ = Category.objects.get_or_create(
            slug="maison", defaults={"name": "Maison"}
        )

        # --- Produits ---
        # Liste de dictionnaires : chaque dict = un produit à créer
        products_data = [
            {
                "name": "T-shirt noir",
                "slug": "t-shirt-noir",
                "description": "T-shirt 100% coton, coupe classique, idéal au quotidien.",
                "price": 29.90,
                "stock": 50,
                "category": vetements,
            },
            {
                "name": "Sweat à capuche gris",
                "slug": "sweat-capuche-gris",
                "description": "Sweat à capuche confortable, parfait pour l'hiver.",
                "price": 79.00,
                "stock": 20,
                "category": vetements,
            },
            {
                "name": "Écouteurs sans fil",
                "slug": "ecouteurs-sans-fil",
                "description": "Écouteurs Bluetooth avec réduction de bruit active.",
                "price": 149.00,
                "stock": 15,
                "category": electronique,
            },
            {
                "name": "Chargeur rapide USB-C",
                "slug": "chargeur-rapide-usb-c",
                "description": "Chargeur 20W compatible avec la majorité des smartphones.",
                "price": 39.50,
                "stock": 0,  # exemple de produit en rupture de stock
                "category": electronique,
            },
            {
                "name": "Lampe de bureau LED",
                "slug": "lampe-bureau-led",
                "description": "Lampe à intensité réglable avec port de charge USB intégré.",
                "price": 59.90,
                "stock": 8,
                "category": maison,
            },
        ]

        for data in products_data:
            # On utilise "slug" comme identifiant unique pour éviter les doublons
            slug = data.pop("slug")
            Product.objects.get_or_create(slug=slug, defaults=data)

        # self.stdout.write : affiche un message dans le terminal
        self.stdout.write(self.style.SUCCESS("Catégories et produits créés avec succès !"))
