from django.db import models
from django.urls import reverse


class Category(models.Model):
    """
    Une catégorie de produits (ex: 'Vêtements', 'Électronique'...).

    On la met dans un modèle séparé (et pas juste un champ texte sur Product)
    pour pouvoir :
    - éviter les doublons / fautes de frappe ("Electronique" vs "Électronique")
    - facilement lister/filtrer les produits par catégorie
    """

    # Le nom affiché de la catégorie (ex: "Chaussures")
    name = models.CharField(max_length=100, unique=True)

    # Le "slug" est une version du nom adaptée aux URLs : minuscules,
    # sans espaces ni accents (ex: "chaussures"). On l'utilisera dans les
    # adresses comme /categorie/chaussures/
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        # Django mettrait "Categorys" au pluriel par défaut, on corrige :
        verbose_name_plural = "categories"
        ordering = ["name"]  # tri alphabétique par défaut

    def __str__(self):
        # __str__ définit comment l'objet s'affiche (ex: dans l'admin Django,
        # dans les listes déroulantes...). Sans ça on verrait "Category object (1)".
        return self.name


class Product(models.Model):
    """
    Un produit vendu sur le site.
    """

    # --- Informations principales ---
    name = models.CharField(max_length=200)

    # Slug unique pour l'URL de la page détail (ex: /produit/t-shirt-noir/)
    slug = models.SlugField(max_length=220, unique=True)

    # TextField = texte long (contrairement à CharField qui est limité)
    description = models.TextField(blank=True)

    # DecimalField est recommandé pour l'argent (jamais FloatField, qui peut
    # provoquer des erreurs d'arrondi). max_digits = nombre total de chiffres,
    # decimal_places = chiffres après la virgule.
    price = models.DecimalField(max_digits=8, decimal_places=2)

    # Quantité disponible en stock. PositiveIntegerField interdit les
    # nombres négatifs (logique pour un stock).
    stock = models.PositiveIntegerField(default=0)

    # --- Image ---
    # blank=True, null=True => le champ est optionnel (utile pour les tests,
    # quand on n'a pas encore d'image). Les fichiers seront stockés dans
    # media/products/.
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    # --- Relation avec Category ---
    # ForeignKey = relation "plusieurs produits -> une catégorie".
    # related_name="products" permet d'écrire : ma_categorie.products.all()
    # on_delete=models.CASCADE => si la catégorie est supprimée, ses produits
    # le sont aussi.
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
    )

    # Permet de "désactiver" un produit sans le supprimer (ex: rupture
    # de stock définitive, produit en pause...).
    available = models.BooleanField(default=True)

    # --- Dates ---
    # auto_now_add = rempli automatiquement à la création, jamais modifié après
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now = mis à jour automatiquement à chaque sauvegarde
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]  # produits les plus récents en premier

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Renvoie l'URL de la page détail de ce produit.
        Pratique pour faire {{ product.get_absolute_url }} dans les templates,
        au lieu d'écrire l'URL "en dur" partout.
        """
        return reverse("product_detail", args=[self.slug])
