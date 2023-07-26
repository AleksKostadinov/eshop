from shop_app.models import Gender, Product, Category
from django.views.generic import ListView, TemplateView, DetailView
from django.urls import reverse


class HomeListView(ListView):
    template_name = 'shop_app/home.html'
    queryset = Product.objects.all()
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        genders = Gender.objects.all()
        context['categories'] = categories
        context['genders'] = genders
        context['products_count'] = self.queryset.count()
        context['just_arrived'] = self.queryset.order_by('-updated_at')[:4]

        return context


class ShopListView(ListView):
    template_name = 'shop_app/shop.html'
    model = Product
    context_object_name = 'products'


class ContactTemplateView(TemplateView):
    template_name = 'shop_app/contact.html'


class ProductDetailView(DetailView):
    template_name = 'shop_app/product_detail.html'
    model = Product

