from .cart import Cart

# This context processor makes the cart available to all templates
def cart(request):
    #Return the default cart data from our cart class
    return {'cart': cart}