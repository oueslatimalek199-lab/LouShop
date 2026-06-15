from django import forms

# Liste de choix pour la quantité : [(1, "1"), (2, "2"), ..., (10, "10")]
# On limite à 10 pour garder un formulaire simple (un menu déroulant).
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]


class CartAddProductForm(forms.Form):
    """
    Formulaire utilisé pour ajouter un produit au panier,
    ou pour modifier sa quantité depuis la page panier.
    """

    # TypedChoiceField : un menu déroulant dont la valeur sera convertie
    # en int grâce à "coerce=int" (sinon on recevrait "3" en texte)
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        label="Quantité",
    )

    # Champ caché qui indique au formulaire ce qu'il faut faire :
    # - update=False (par défaut) -> on AJOUTE cette quantité au panier
    #   (cas de la page produit)
    # - update=True -> on REMPLACE la quantité existante
    #   (cas de la page panier, quand on change la quantité d'un article)
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput,
    )
