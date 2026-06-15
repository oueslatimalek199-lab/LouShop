from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """
    Formulaire de checkout : demande juste les infos de livraison.
    L'utilisateur (user) et le contenu (items) sont gérés dans la vue,
    pas dans ce formulaire.
    """

    class Meta:
        model = Order
        fields = ["full_name", "email", "address", "city"]
