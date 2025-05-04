from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

def cart_summary(request):
    return render(request, "cart_summary.html", {})

def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Get product id
        producy_id = int(request.POST.get('product_id'))
        # Look up product in DB
        product = get_object_or_404(Product, id=producy_id)
        # Save to a session
        cart.add(product=product)
        # Return response
        response = JsonResponse({ 'Product Name: ': product.name })
        return response


    
       

def cart_delete(request):
    pass

def cart_update(request):
    pass