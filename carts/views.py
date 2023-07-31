from decimal import Decimal
from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from orders.models import Order, ShippingConfig

from shop_app.models import Product
from .models import Cart, CartItem

class CartView(View):
    template_name = 'carts/carts.html'

    def get_cart(self, request):
        # Get or create the cart for the current user
        cart, created = Cart.objects.get_or_create(user=request.user, purchased=False)
        return cart

    def get_cart_items(self, cart):
        # Retrieve cart items associated with the given cart
        cart_items = CartItem.objects.filter(cart=cart)
        return cart_items

    def sum_wo_shipping(self, cart_items):
        sum_wo_shipping = sum(item.sub_total() for item in cart_items)
        return sum_wo_shipping

    def get_total_sum(self, cart_items):
        # Retrieve the shipping cost configuration from the ShippingConfig model
        shipping_config = ShippingConfig.objects.first()  # You can modify the query based on your requirement

        # Convert shipping_cost_percent to Decimal before calculation
        shipping_cost_percent_decimal = Decimal(str(shipping_config.shipping_cost_percent))

        # Calculate the shipping cost based on the total sum and shipping_cost_percent
        shipping_cost = self.sum_wo_shipping(cart_items) * (shipping_cost_percent_decimal / 100)
        total_sum = shipping_cost + self.sum_wo_shipping(cart_items)
        return shipping_cost, total_sum

    def get(self, request, *args, **kwargs):
        # Get the cart for the current user
        cart = self.get_cart(request)

        # Get cart items for the cart
        cart_items = self.get_cart_items(cart)

        # Fetch the shipping cost percentage from the Order model
        try:
            order = Order.objects.get(user=request.user, is_ordered=False)
            shipping_cost_percent = order.shipping_cost_percent
        except Order.DoesNotExist:
            shipping_cost_percent = 0

        sum_wo_shipping = self.sum_wo_shipping(cart_items)

        # Calculate the total sum of all cart items
        shipping_cost, total_sum = self.get_total_sum(cart_items)

        context = {
            'cart': cart,
            'cart_items': cart_items,
            'sum_wo_shipping': sum_wo_shipping,
            'shipping_cost': shipping_cost,
            'total_sum': total_sum,
        }

        return render(request, self.template_name, context)


class AddToCartView(View):
    def post(self, request, product_id):
        # Get the selected product
        product = get_object_or_404(Product, id=product_id)

        # Check if the user has an active cart
        cart, created = Cart.objects.get_or_create(user=request.user, purchased=False)

        # Add the product to the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()

        # Show success message after adding the product to the cart
        messages.success(request, f"{product.product_name} has been added.")

        return redirect('carts:carts')
