from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product
from .models import Cart, CartItem


@login_required(login_url='login')
def view_cart(request):
    """Affiche le panier de l'utilisateur"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    context = {
        'cart': cart,
        'cart_items': cart.items.select_related('product'),
        'total_price': cart.get_total_price(),
        'total_items': cart.get_total_items(),
    }
    return render(request, 'cart/view_cart.html', context)


@login_required(login_url='login')
def add_to_cart(request, product_id):
    """Ajoute un produit au panier"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    quantity = int(request.POST.get('quantity', 1))
    quantity = max(1, min(quantity, product.stock))
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.quantity = min(cart_item.quantity, product.stock)
        cart_item.save()
    
    messages.success(request, f"{product.name} ajouté au panier.")
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f"{product.name} ajouté au panier",
            'cart_total_items': cart.get_total_items(),
        })
    
    return redirect('view_cart')


@login_required(login_url='login')
def update_cart_item(request, item_id):
    """Met à jour la quantité d'un article du panier"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        cart_item.delete()
        messages.info(request, f"{cart_item.product.name} supprimé du panier.")
    else:
        quantity = min(quantity, cart_item.product.stock)
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Quantité mise à jour.")
    
    return redirect('view_cart')


@login_required(login_url='login')
def remove_from_cart(request, item_id):
    """Supprime un article du panier"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f"{product_name} supprimé du panier.")
    return redirect('view_cart')


@login_required(login_url='login')
def clear_cart(request):
    """Vide complètement le panier"""
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    messages.success(request, "Panier vidé.")
    return redirect('view_cart')
