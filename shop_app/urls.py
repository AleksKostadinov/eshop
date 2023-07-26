from django.urls import path
from .views import Home

app_name = 'shop_app'

urlpatterns = [
    # path('', views.home, name='home'),
    path('', Home.as_view(), name='home'),
]

