
class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get the cart from the session
        cart = self.session.get('session_key')
        # If the session doesn't exist, create a new one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        # Making cart available to all pages of site
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        # Logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price': str(product.price)}

        self.session.modified = True