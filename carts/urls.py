from django.urls import path
from carts.views import CartView
from .views import AddToCartView

app_name = 'carts'

urlpatterns = [
    path('', CartView.as_view(), name='carts'),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
]
