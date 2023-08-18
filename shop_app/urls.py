from django.urls import path
from .views import (HomeListView, ShopListView, ContactView,
                    ProductDetailView, GenderListView, CategoryListView,
                    CategoryGenderListView, ProductSearchView, SubmitReviewView,
                    CollectionListView)

app_name = 'shop_app'

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('shop/', ShopListView.as_view(), name='shop'),
    path('shop/category/<slug:category_slug>/', CategoryListView.as_view(), name='shop_by'),
    path('shop/gender/<slug:gender_slug>/', GenderListView.as_view(), name='shop_by'),
    path('shop/collection/<slug:collection_slug>/', CollectionListView.as_view(), name='shop_by'),
    path('shop/<slug:category_slug>/<slug:gender_slug>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('shop/<slug:category_slug>/<slug:gender_slug>/', CategoryGenderListView.as_view(), name='shop_by'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('search/', ProductSearchView.as_view(), name='product_search'),
    path('submit_review/<int:product_id>/', SubmitReviewView.as_view(), name='submit_review'),
    # path('filtered_products/', filtered_products, name='filtered_products')
]

