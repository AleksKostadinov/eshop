from django.urls import path
from carts.views import CartView
from .views import AddToCartView, RemoveCartView, RemoveCartItemView

app_name = 'carts'

urlpatterns = [
    path('', CartView.as_view(), name='carts'),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', RemoveCartView.as_view(), name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', RemoveCartItemView.as_view(), name='remove_cart_item'),

]
