# ShopLine — Simple E-commerce Store (Task 1)

Projet réalisé dans le cadre du stage Full Stack Development chez **CodeAlpha**.

## Stack
- Backend : **Django** (Python)
- Frontend : HTML, CSS, JavaScript (templates Django)
- Base de données : SQLite (par défaut, en développement)

## Fonctionnalités prévues
- [x] Setup du projet
- [ ] Listing produits + page détail produit
- [ ] Authentification (inscription / connexion)
- [ ] Panier
- [ ] Traitement des commandes

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
├── accounts/     # inscription, connexion, profils
├── products/     # produits, catégories, page détail
├── cart/         # panier
├── orders/       # traitement des commandes
├── templates/    # HTML partagés (base.html, pages)
└── static/       # CSS, JS
```
