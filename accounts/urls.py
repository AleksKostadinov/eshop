from django.urls import path
from accounts.views import CustomLoginView, CustomRegisterView

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', CustomRegisterView.as_view(), name='register'),
]

