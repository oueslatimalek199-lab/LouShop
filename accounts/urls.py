from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Inscription : vue personnalisée (accounts/views.py)
    path("inscription/", views.register, name="register"),

    # Connexion : on réutilise la vue LoginView fournie par Django,
    # en lui donnant juste notre propre template.
    path(
        "connexion/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),

    # Déconnexion : vue LogoutView fournie par Django.
    # Depuis Django 5, LogoutView n'accepte QUE le POST (pour éviter qu'un
    # simple lien <a> ou un robot ne déconnecte l'utilisateur par accident).
    # C'est pour ça qu'on utilisera un <form method="post"> dans la navbar.
    path("deconnexion/", auth_views.LogoutView.as_view(), name="logout"),
]
