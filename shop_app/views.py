from shop_app.models import Gender, Product, Category
from django.views.generic import ListView


class Home(ListView):
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
