# ShopLine — Simple E-commerce Store (Task 1)

Projet réalisé dans le cadre du stage Full Stack Development chez **CodeAlpha**.

## Stack
- Backend : **Django** (Python)
- Frontend : HTML, CSS, JavaScript (templates Django)
- Base de données : SQLite (par défaut, en développement)

## Fonctionnalités
- [x] Setup du projet
- [x] Listing produits + page détail produit (avec filtre par catégorie)
- [x] Panier (ajout, modification de quantité, suppression, basé sur la session)
- [x] Authentification (inscription / connexion / déconnexion)
- [x] Traitement des commandes (checkout, confirmation, historique, décrément du stock)

## Installation et lancement en local

```bash
# 1. Cloner le projet
git clone https://github.com/oueslatimalek199-lab/shopline.git
cd shopline

# 2. Créer et activer un environnement virtuel
python -m venv venv

# Sur Windows :
venv\Scripts\activate
# Sur Mac/Linux :
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Appliquer les migrations
python manage.py migrate

# 5. (Optionnel) créer un compte admin
python manage.py createsuperuser

# 6. Lancer le serveur
python manage.py runserver
```

Le site sera disponible sur http://127.0.0.1:8000/

## Structure du projet

```
ecommerce_project/
├── accounts/     # inscription, connexion, déconnexion
├── products/     # produits, catégories, page détail
├── cart/         # panier (basé sur la session)
├── orders/       # checkout, confirmation, historique des commandes
├── templates/    # HTML partagés (base.html, pages de chaque app)
└── static/       # CSS, images
```

## Comptes de test

Crée un compte admin pour gérer produits/catégories/commandes via `/admin/` :
```bash
python manage.py createsuperuser
```

Les visiteurs peuvent créer un compte via `/compte/inscription/`.

## Parcours utilisateur
1. Page d'accueil (`/`) : liste des produits, filtre par catégorie
2. Page produit (`/produit/<slug>/`) : détail + ajout au panier
3. Panier (`/panier/`) : modifier quantités, retirer, voir le total
4. Checkout (`/commande/commander/`) — nécessite d'être connecté
5. Confirmation puis historique (`/commande/mes-commandes/`)
