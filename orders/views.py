from datetime import date
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from carts.models import CartItem
from carts.views import BaseCartView
from orders.forms import OrderForm
from orders.models import Order, OrderProduct, Payment
from django.contrib.auth.mixins import LoginRequiredMixin
from shop_app.models import Product
from django.contrib import messages
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class PaymentsView(View):
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

        # Store transaction details inside Payment model
        payment = Payment(
            user=request.user,
            payment_id=body['transID'],
            payment_method=body['payment_method'],
            amount_paid=order.order_total,
            status=body['status'],
        )
        payment.save()

        order.payment = payment
        order.is_ordered = True
        order.save()

        # Move the cart items to Order Product table
        cart_items = CartItem.objects.filter(cart__user=request.user)

        for item in cart_items:
            orderproduct = OrderProduct(
                order=order,
                payment=payment,
                user=request.user,
                product_id=item.product_id,
                quantity=item.quantity,
                product_price=item.product.discounted_price_db,
                ordered=True,
            )
            orderproduct.save()
            orderproduct.variations.set(item.variations.all())

            # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.quantity -= item.quantity
            product.save()

        # Clear cart
        CartItem.objects.filter(cart__user=request.user).delete()



        # Send order number and transaction id back to sendData method via JsonResponse
        data = {
            'order_number': order.order_number,
            'transID': payment.payment_id,
        }
        return JsonResponse(data)


class PlaceOrderView(BaseCartView, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        current_user = request.user
        base_cart_view = BaseCartView()
        cart = base_cart_view.get_cart(request)
        cart_items = base_cart_view.get_cart_items(cart)

        for item in cart_items:
            if item.product.quantity <= 0:
                messages.error(request, f"Product '{item.product.product_name}' is out of stock.")
                return redirect('carts:carts')

        total = base_cart_view.sum_wo_shipping(cart_items)
        tax, grand_total = base_cart_view.get_total_sum(cart_items)

        tax = int(tax * 100) / 100
        total = int(total * 100) / 100
        grand_total = total + tax

        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number
            yr = int(date.today().strftime('%Y'))
            dt = int(date.today().strftime('%d'))
            mt = int(date.today().strftime('%m'))
            d = date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)

    def get(self, request, *args, **kwargs):
        return redirect('carts:checkout')


class OrderCompleteView(View):
    def get(self, request, *args, **kwargs):
        order_number = request.GET.get('order_number')
        transID = request.GET.get('payment_id')

        try:
            order = Order.objects.get(order_number=order_number, is_ordered=True)
            ordered_products = OrderProduct.objects.filter(order_id=order.id)

            subtotal = sum(i.product_price * i.quantity for i in ordered_products)

            payment = Payment.objects.get(payment_id=transID)

            subject = 'Thank you for your order!'
            message = render_to_string('orders/order_received_email.html', {
                'user': request.user,
                'order': order,
                'ordered_products': ordered_products,
                'subtotal': subtotal,
            })
            to_email = request.user.email
            send_email = EmailMessage(subject, message, to=[to_email])
            send_email.send()
            print(subtotal)
            context = {
                'order': order,
                'ordered_products': ordered_products,
                'order_number': order.order_number,
                'transID': payment.payment_id,
                'payment': payment,
            }
            return render(request, 'orders/order_complete.html', context)
        except (Payment.DoesNotExist, Order.DoesNotExist):
            return redirect('shop_app:home')
