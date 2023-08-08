from django.urls import path
from orders.views import PlaceOrderView, payments, order_complete

app_name = 'orders'

urlpatterns = [
    path('place_order/', PlaceOrderView.as_view(), name='place_order'),
    # path('payments/', PaymentsView.as_view(), name='payments'),
    path('payments/', payments, name='payments'),
    path('order_complete/', order_complete, name='order_complete'),
]
