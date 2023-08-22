from django.urls import path
from .views import (CustomLoginView, CustomRegisterView, CustomLogoutView,
                    DashboardView, MyOrdersView, EditProfileView,
                    ChangePasswordView, OrderDetailView, SubscribeView,
                    UnsubscribeView)

app_name = 'accounts'

urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', DashboardView.as_view(), name='dashboard'),

    path('my_orders/', MyOrdersView.as_view(), name='my_orders'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('order_detail/<int:order_number>/', OrderDetailView.as_view(), name='order_detail'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('unsubscribe/', UnsubscribeView.as_view(), name='unsubscribe'),
]
