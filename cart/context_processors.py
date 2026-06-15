"""
Un "context processor" injecte automatiquement une variable dans TOUS les
templates, sans avoir à la passer manuellement dans chaque vue.

On l'utilise ici pour que la navbar (dans base.html) puisse afficher le
nombre d'articles dans le panier, sur n'importe quelle page du site.

Il faut l'enregistrer dans settings.py (voir TEMPLATES -> context_processors).
"""

from .cart import Cart


def cart(request):
    return {"cart": Cart(request)}
