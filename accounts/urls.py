from django.urls import path
from .views import CustomLoginView, CustomRegisterView, CustomLogoutView

app_name = 'accounts'

urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
