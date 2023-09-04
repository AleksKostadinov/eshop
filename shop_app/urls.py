from django.urls import path

from .views import (CategoryGenderListView, CategoryListView,
                    CollectionListView, ContactView, GenderListView,
                    HomeListView, NewsletterView, ProductDetailView,
                    ProductSearchView, ShopListView, SubmitReviewView)

app_name = 'shop_app'

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('shop/', ShopListView.as_view(), name='shop'),
    path('shop/category/<slug:category_slug>/', CategoryListView.as_view(), name='shop'),
    path('shop/gender/<slug:gender_slug>/', GenderListView.as_view(), name='shop'),
    path('shop/collection/<slug:collection_slug>/', CollectionListView.as_view(), name='shop'),
    path('shop/<slug:category_slug>/<slug:gender_slug>/', CategoryGenderListView.as_view(), name='shop'),
    path('shop/<slug:gender_slug>/<slug:category_slug>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('search/', ProductSearchView.as_view(), name='product_search'),
    path('submit_review/<int:product_id>/', SubmitReviewView.as_view(), name='submit_review'),
    path('newsletter/', NewsletterView.as_view(), name='newsletter'),
]

