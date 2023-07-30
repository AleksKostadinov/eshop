from django.shortcuts import get_object_or_404
from shop_app.forms import ContactForm
from shop_app.models import Gender, Product, Category
from django.views.generic import ListView, TemplateView, DetailView, FormView
from django.urls import reverse, reverse_lazy
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


class ProductsMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        context['products'] = products
        return context


class CategoryGenderBaseView():
    template_name = 'shop_app/shop_by.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        genders = Gender.objects.annotate(product_count=Count('product'))
        context['categories'] = categories
        context['genders'] = genders
        return context


class HomeListView(CategoryGenderBaseView, ListView):
    template_name = 'shop_app/home.html'
    model = Product
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products_count'] = self.model.objects.count()
        context['just_arrived'] = self.model.objects.order_by('-updated_at')[:4]
        return context


class ShopListView(CategoryGenderBaseView, ListView):
    template_name = 'shop_app/shop.html'
    model = Product


class ProductDetailView(ProductsMixin, CategoryGenderBaseView, DetailView):
    template_name = 'shop_app/product_detail.html'
    model = Product
    context_object_name = 'product'


class GenderListView(CategoryGenderBaseView, ListView):
    def get_queryset(self):
        gender_slug = self.kwargs.get('gender_slug')
        gender = get_object_or_404(Gender, slug=gender_slug)

        return Product.objects.filter(gender=gender)


class CategoryListView(CategoryGenderBaseView, ListView):
    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(Category, slug=category_slug)

        return Product.objects.filter(category=category)


class CategoryGenderListView(CategoryGenderBaseView, ListView):
    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        gender_slug = self.kwargs.get('gender_slug')
        category = get_object_or_404(Category, slug=category_slug)
        gender = get_object_or_404(Gender, slug=gender_slug)

        return Product.objects.filter(category=category, gender=gender)


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'shop_app/contact.html'
    success_url = reverse_lazy('shop_app:home')

    def form_valid(self, form):
        self.send_mail(form.cleaned_data)
        return super(ContactView, self).form_valid(form)

    def send_mail(self, valid_data):
        name = valid_data['name']
        email = valid_data['email']
        subject = valid_data['subject']
        message = valid_data['message']

        # Create the email content
        email_content = f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}"

        # Send the email
        try:
            send_mail(
                subject="Contact Form Submission",
                message=email_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_REDIRECT_TO],
            )
        except Exception as e:
            # Handle email sending errors if needed
            messages.error(self.request, f"Error sending email: {e}")
        else:
            messages.success(self.request, "Email sent successfully!")
