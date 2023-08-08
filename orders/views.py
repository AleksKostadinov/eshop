from datetime import date

from django.shortcuts import get_object_or_404, redirect, render

from carts.views import BaseCartView
from orders.forms import OrderForm
from orders.models import Order, OrderProduct, Payment
from django.contrib.auth.mixins import LoginRequiredMixin




def payments(request):
    pass

# class PaymentsView(LoginRequiredMixin, View):

#     def get(self, request, *args, **kwargs):
#         body = json.loads(request.body)

#         order_number = body.get('order_number')
#         order = get_object_or_404(Order, order_number=order_number)
#         context = {
#             'order': order,
#         }


class PlaceOrderView(BaseCartView, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        current_user = request.user
        base_cart_view = BaseCartView()
        cart = base_cart_view.get_cart(request)
        cart_items = base_cart_view.get_cart_items(cart)
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


def order_complete(request):
    pass
