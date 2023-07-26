from django.shortcuts import render

from shop_app.models import Product
from django.views.generic import ListView


# def home(request):
#     return render(request, 'shop_app/home.html')

class Home(ListView):
    model = Product
    template_name = 'shop_app/home.html'