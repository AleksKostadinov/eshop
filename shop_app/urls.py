from django.urls import path
from .views import HomeListView, ShopListView, ContactTemplateView, ProductDetailView, GenderListView, CategoryListView

app_name = 'shop_app'

urlpatterns = [
    # path('', views.home, name='home'),
    path('', HomeListView.as_view(), name='home'),
    path('shop/', ShopListView.as_view(), name='shop'),
    path('shop/<slug:gender_slug>/<slug:category_slug>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('shop/<slug:gender_slug>/', GenderListView.as_view(), name='shop_by_gender'),
    path('shop/category/<slug:category_slug>/', CategoryListView.as_view(), name='shop_by_category'),
    path('contact/', ContactTemplateView.as_view(), name='contact'),
]

