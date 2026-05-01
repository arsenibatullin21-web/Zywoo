import copy
from decimal import Decimal

from Zywoo import settings
from main.models import Product


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, product ,color, size, override_quantity = False):
        cart_key = f"{product.id}_{color.id}_{size.id}"

        if cart_key not in self.cart:
            self.cart[cart_key] = {
                'quantity': 0,
                'product_id': product.id,
                'price': str(product.final_price),
                'color_name': str(color.name),
                'color_id': color.id,
                'size_name': str(size.name),
                'size_id': size.id,
            }

        if override_quantity:
            self.cart[cart_key]['quantity'] = 1
        else:
            self.cart[cart_key]['quantity'] += 1

        self.save()

    def delete(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def clear_items(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.save()

    def remove(self, cart_key):
        if cart_key in self.cart:
            del self.cart[cart_key]
        self.save()

    def get_total(self):
        total = Decimal('0.00')
        for item in self.cart.values():
            total += Decimal(item['quantity']) * Decimal(item['price'])
        return total

    def update_quantity(self, cart_key, action):
        if cart_key in self.cart:
            if action == 'increase':
                self.cart[cart_key]['quantity'] += 1
            elif action == 'decrease':
                self.cart[cart_key]['quantity'] -= 1
                if self.cart[cart_key]['quantity'] < 1:
                    del self.cart[cart_key]
        self.save()

    def __iter__(self):
        product_ids = [item['product_id'] for item in self.cart.values()]
        products = Product.objects.filter(id__in=product_ids)
        cart = copy.deepcopy(self.cart)


        for key, item in cart.items():
            item['cart_key'] = key

        for product in products:
            for item in cart.values():
                if product.id == item['product_id']:
                    item['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

