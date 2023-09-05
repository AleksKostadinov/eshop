from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from orders.models import Order, ShippingConfig
from shop_app.models import Product, Variation

from .models import Cart, CartItem


class BaseCartView(LoginRequiredMixin, View):
    def get_cart(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Get or create the cart for the current user
            cart, created = Cart.objects.get_or_create(user=request.user, purchased=False)
        else:
            # If the user is not authenticated, set the user_id to None or any default value
            cart = None
        return cart

    def get_cart_items(self, cart):
        # Check if cart is not None (for unauthenticated users, cart will be None)
        if cart:
            # Retrieve cart items associated with the given cart
            cart_items = CartItem.objects.filter(cart=cart).order_by('-id')
        else:
            # If cart is None (for unauthenticated users), return an empty queryset
            cart_items = CartItem.objects.none()
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


class CartView(BaseCartView):
    template_name = 'carts/carts.html'

    def get(self, request, *args, **kwargs):

        # Get the cart for the current user
        cart = self.get_cart(request)

        # Get cart items for the cart
        cart_items = self.get_cart_items(cart)

        # Fetch the shipping cost percentage from the Order model
        # try:
        #     order = get_object_or_404(Order, user=request.user, is_ordered=False)
        #     shipping_cost_percent = order.shipping_cost_percent
        # except Order.DoesNotExist:
        #     shipping_cost_percent = 0

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



# def _cart_id(request):
#     cart = request.session.session_key
#     if not cart:
#         cart = request.session.create()
#     return cart

def message_added_product(request, product, variation_info):
    message = f"Product: {product.product_name} , "

    message += ", ".join(variation_info)

        # Show the success message
    message += " has been added to your cart."
    messages.success(request, message)


class AddToCartView(BaseCartView):
    login_url = '/accounts/login/'

    def post(self, request, product_id):
        cart = self.get_cart(request)
        product = get_object_or_404(Product, id=product_id)

        product_variations = []
        variation_info = []
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variations.append(variation)
                variation_info.append(f"{variation.variation_category.capitalize()}: {variation.variation_value}")
            except Variation.DoesNotExist:
                pass


        if cart is None:
            # Create a new cart for the user if it doesn't exist
            cart = Cart.objects.create(user=request.user)

        # Find cart items with the same product and same size
        matching_cart_items = CartItem.objects.filter(
            cart=cart,
            product=product,
            is_active=True,
            variations__variation_category='size',  # Filter by size variation
            variations__in=product_variations,
        ).distinct()

        for matching_cart_item in matching_cart_items:
            # Check if the matching cart item has the same color variation
            matching_color_variations = matching_cart_item.variations.filter(
                variation_category='color',  # Filter by color variation
                variation_value__in=[v.variation_value for v in product_variations if v.variation_category == 'color']
            )
            if matching_color_variations.count() == len(product_variations) - 1:
                # If all color variations match, increase the quantity
                matching_cart_item.quantity += 1
                matching_cart_item.save()
                message_added_product(request, product, variation_info)

                return redirect('carts:carts')

        # If no matching cart item is found, create a new cart item for the product with the selected variations
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
        cart_item.variations.add(*product_variations)

        # Construct the success message with product name and variation information
        message_added_product(request, product, variation_info)

        return redirect('carts:carts')

class RemoveCartView(View):
    def post(self, request, product_id, cart_item_id):
        product = get_object_or_404(Product, id=product_id)
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        except Cart.DoesNotExist:
            pass
        except CartItem.DoesNotExist:
            pass
        return redirect('carts:carts')

class RemoveCartItemView(View):
    def post(self, request, product_id, cart_item_id):
        product = get_object_or_404(Product, id=product_id)
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
            cart_item.delete()
        except Cart.DoesNotExist:
            pass
        except CartItem.DoesNotExist:
            pass
        return redirect('carts:carts')

class CheckoutView(CartView):
    template_name = 'carts/checkout.html'
