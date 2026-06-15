from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """
    Formulaire d'inscription.

    UserCreationForm est un formulaire fourni par Django qui gère déjà :
    - le champ "username"
    - les deux champs mot de passe ("password1" et "password2")
    - la vérification que les deux mots de passe correspondent
    - les règles de sécurité (longueur minimale, mot de passe trop courant, etc.)

    On y ajoute juste un champ "email".
    """

    email = forms.EmailField(required=True, label="Adresse email")

    class Meta(UserCreationForm.Meta):
        model = User
        # Ordre des champs affichés dans le formulaire
        fields = ["username", "email", "password1", "password2"]
