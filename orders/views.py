from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from cart.models import Cart, CartItem
from .models import Order, OrderItem
import uuid


@login_required(login_url='login')
def checkout(request):
    """Page de paiement/confirmation de commande"""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.select_related('product')
    
    if not cart_items.exists():
        messages.warning(request, "Votre panier est vide.")
        return redirect('view_cart')
    
    if request.method == 'POST':
        # Récupérer les données du formulaire
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')
        phone_number = request.POST.get('phone_number')
        
        # Validation basique
        if not all([address, city, zip_code, country, phone_number]):
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, 'orders/checkout.html', {
                'cart_items': cart_items,
                'cart_total': cart.get_total_price(),
            })
        
        # Créer la commande
        with transaction.atomic():
            order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
            subtotal = cart.get_total_price()
            shipping_cost = 0  # À adapter selon votre logique
            total_amount = subtotal + shipping_cost
            
            order = Order.objects.create(
                user=request.user,
                order_number=order_number,
                address=address,
                city=city,
                zip_code=zip_code,
                country=country,
                phone_number=phone_number,
                subtotal=subtotal,
                shipping_cost=shipping_cost,
                total_amount=total_amount,
            )
            
            # Créer les articles de la commande
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    product_name=cart_item.product.name,
                    price=cart_item.product.price,
                    quantity=cart_item.quantity,
                )
                
                # Réduire le stock
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()
            
            # Vider le panier
            cart_items.delete()
            
            messages.success(request, f"Commande créée avec succès : {order_number}")
            return redirect('order_confirmation', order_id=order.id)
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart.get_total_price(),
        'user_profile': request.user.profile,
    }
    return render(request, 'orders/checkout.html', context)


@login_required(login_url='login')
def order_confirmation(request, order_id):
    """Affiche la confirmation de commande"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'orders/confirmation.html', context)


@login_required(login_url='login')
def order_history(request):
    """Affiche l'historique des commandes de l'utilisateur"""
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/history.html', context)


@login_required(login_url='login')
def order_detail(request, order_id):
    """Affiche les détails d'une commande"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'orders/detail.html', context)
