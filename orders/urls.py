from django.urls import path
from . import views

urlpatterns = [
    # http://127.0.0.1:8000/commande/commander/  (checkout)
    path("commander/", views.order_create, name="order_create"),

    # http://127.0.0.1:8000/commande/confirmation/5/
    path("confirmation/<int:order_id>/", views.order_created, name="order_created"),

    # http://127.0.0.1:8000/commande/mes-commandes/
    path("mes-commandes/", views.order_list, name="order_list"),
]
