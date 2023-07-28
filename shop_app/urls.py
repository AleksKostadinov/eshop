from django.urls import path
from .views import HomeListView, ShopListView, ContactTemplateView, ProductDetailView, GenderListView, CategoryListView, CategoryGenderListView

app_name = 'shop_app'

urlpatterns = [
    # path('', views.home, name='home'),
    path('', HomeListView.as_view(), name='home'),
    path('shop/', ShopListView.as_view(), name='shop'),
    path('shop/category/<slug:category_slug>/', CategoryListView.as_view(), name='shop_by'),
    path('shop/gender/<slug:gender_slug>/', GenderListView.as_view(), name='shop_by'),
    path('shop/<slug:category_slug>/<slug:gender_slug>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('shop/<slug:category_slug>/<slug:gender_slug>/', CategoryGenderListView.as_view(), name='shop_by'),
    path('contact/', ContactTemplateView.as_view(), name='contact'),
]

