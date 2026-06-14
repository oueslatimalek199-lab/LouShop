from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category


def home(request):
    """Page d'accueil — affiche la liste des produits"""
    products_list = Product.objects.filter(is_active=True).select_related('category')
    
    # Filtrer par catégorie si spécifiée
    category_id = request.GET.get('category')
    if category_id:
        products_list = products_list.filter(category_id=category_id)
    
    # Recherche par nom
    search_query = request.GET.get('search')
    if search_query:
        products_list = products_list.filter(name__icontains=search_query)
    
    # Pagination
    paginator = Paginator(products_list, 12)  # 12 produits par page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query or '',
        'selected_category': int(category_id) if category_id else None,
    }
    return render(request, 'products/home.html', context)


def product_detail(request, product_id):
    """Affiche les détails d'un produit"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product_id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)
