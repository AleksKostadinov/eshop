from django.urls import path
from orders.views import PlaceOrderView,PaymentsView, OrderCompleteView

app_name = 'orders'

urlpatterns = [
    path('place_order/', PlaceOrderView.as_view(), name='place_order'),
    path('payments/', PaymentsView.as_view(), name='payments'),
    path('order_complete/', OrderCompleteView.as_view(), name='order_complete'),
]
