
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

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def clear_cart(self):
        self.items = []

    def get_items(self):
        return self.items

    def get_total_price(self):
        return sum(item['price'] for item in self.items)