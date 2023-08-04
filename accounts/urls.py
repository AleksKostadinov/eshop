from django.urls import path
from .views import CustomLoginView, CustomRegisterView, CustomLogoutView, register

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    # path('register/', CustomRegisterView.as_view(), name='register'),
    path('register/', register, name='register'),
]

