from store.models import Product, Profile


class Cart():
    def __init__(self, request):
        # Get the cart from the session
        self.session = request.session
        # Get the request
        self.request = request
        cart = self.session.get('session_key')
        # If the session doesn't exist, create a new one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        # Making cart available to all pages of site
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        # Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert single quotes to double quotes
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to Profile Model
            current_user.update(old_cart=str(carty))
             

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        # Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert single quotes to double quotes
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to Profile Model
            current_user.update(old_cart=str(carty))

    def cart_total(self):
        # Get product ID's
        product_ids = self.cart.keys()
        # Lookup those keys in our products 
        products = Product.objects.filter(id__in=product_ids)
        # Get quantities
        quantities = self.cart
        total = 0

        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total
        

    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        # Get IDs from cart
        product_ids = self.cart.keys()
        # Use ids to get products in Database model
        products = Product.objects.filter(id__in=product_ids)

        # Return the products in cart
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        # Get cart to update
        current_cart = self.cart
        # update our dicationary/cart
        current_cart[product_id] = product_qty

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert single quotes to double quotes
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to Profile Model
            current_user.update(old_cart=str(carty))

        updated_cart = self.cart
        return updated_cart
    
    def delete(self, product):
        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert single quotes to double quotes
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to Profile Model
            current_user.update(old_cart=str(carty))
        