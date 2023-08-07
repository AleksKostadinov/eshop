from django.urls import path
from orders.views import PlaceOrderView

app_name = 'orders'

urlpatterns = [
    path('place_order/', PlaceOrderView.as_view(), name='place_order'),
]

