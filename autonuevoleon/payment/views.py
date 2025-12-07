from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem



def process_order(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        # Get Billing info from last page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')

        # Get Order info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']

        # Create Shipping Addres`s from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
        amount_paid = totals

        # Create an order
        if request.user.is_authenticated:
            # User is logged in
            user = request.user
            # Create Order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            messages.success(request, "Order Placed")
            return redirect('home')
        else:
            # Not Logged in user
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            messages.success(request, "Order Placed")
            return redirect('home')
        

    else:
        messages.success(request, "Access Denied")
        return redirect('home')

def billing_info(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Create a session with Shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # Check to see if user is logged in
        if request.user.is_authenticated:
            # Get the Billing Form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})
            
        else:
            # Not logged in user
            # Get the Billing Form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})


        shipping_form = request.POST
        return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def checkout(request):

    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # Chekout as logged in User
        # Shipping User
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
    else:
        # Checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})



def payment_success(request):
    
    return render(request, "payment/payment_success.html", {})
