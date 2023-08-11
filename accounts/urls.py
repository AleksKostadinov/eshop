from django.urls import path
from .views import CustomLoginView, CustomRegisterView, CustomLogoutView, DashboardView, MyOrdersView, EditProfileView

app_name = 'accounts'

urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', DashboardView.as_view(), name='dashboard'),

    path('my_orders/', MyOrdersView.as_view(), name='my_orders'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
]
