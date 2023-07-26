from django.shortcuts import render
from django.views import View

class CartView(View):
    template_name = 'carts/carts.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
