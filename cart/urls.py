from django.urls import path
from . import views

urlpatterns = [
    # http://127.0.0.1:8000/panier/
    path("", views.cart_detail, name="cart_detail"),

    # http://127.0.0.1:8000/panier/ajouter/3/  (3 = id du produit)
    path("ajouter/<int:product_id>/", views.cart_add, name="cart_add"),

    # http://127.0.0.1:8000/panier/retirer/3/
    path("retirer/<int:product_id>/", views.cart_remove, name="cart_remove"),
]
