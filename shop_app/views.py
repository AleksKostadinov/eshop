from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from carts.models import CartItem
from orders.models import OrderProduct
from shop_app.forms import ContactForm, ReviewForm
from shop_app.models import Collection, Gender, Product, Category, ProductGallery, ReviewRating
from django.views.generic import ListView, DetailView, FormView
from django.urls import reverse_lazy
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.db.models import Avg, Count, F


def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request, exception):
    return render(request, '500.html', status=500)

class ProductsMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        context['products'] = products
        return context


class CategoryGenderBaseView():
    template_name = 'shop_app/shop_by.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        genders = Gender.objects.annotate(product_count=Count('product'))
        collections = Collection.objects.all()
        context['categories'] = categories
        context['genders'] = genders
        context['collections'] = collections
        return context


class HomeListView(CategoryGenderBaseView, ListView):
    template_name = 'shop_app/home.html'
    model = Product
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_products = Product.objects.top_by_rating()
        context['top_products'] = top_products
        context['products_count'] = self.model.objects.count()
        context['just_arrived'] = self.model.objects.order_by('-created_at')[:4]
        return context


# class ShopListView(CategoryGenderBaseView, ListView):
#     template_name = 'shop_app/shop.html'
#     model = Product


#     def get_queryset(self):
#         sort_param = self.request.GET.get('sort', 'latest')  # Default to sorting by latest
#         queryset = Product.objects.all()

#         if sort_param == 'latest':
#             queryset = queryset.order_by('-created_at')
#         elif sort_param == 'reviews':
#             queryset = queryset.annotate(review_count=Count('reviewrating')).order_by('-review_count')
#         elif sort_param == 'rating':
#             queryset = queryset.annotate(average_rating=Avg('reviewrating__rating')).order_by('-average_rating')
#         return queryset


class ShopListView(CategoryGenderBaseView, ListView):
    template_name = 'shop_app/shop.html'
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get filter parameters from the request
        price_filter = self.request.GET.get('price')
        color_filter = self.request.GET.get('color')
        size_filter = self.request.GET.get('size')
        sort_filter = self.request.GET.get('sort')

        # Apply filters based on selected options
        if price_filter:
            if price_filter == 'price-1':
                queryset = queryset.filter(discounted_price_db__range=(0, 99.99))
            elif price_filter == 'price-2':
                queryset = queryset.filter(discounted_price_db__range=(100, 199.99))
            elif price_filter == 'price-3':
                queryset = queryset.filter(discounted_price_db__range=(200, 299.99))
            elif price_filter == 'price-4':
                queryset = queryset.filter(discounted_price_db__range=(300, 399.99))
            elif price_filter == 'price-5':
                queryset = queryset.filter(discounted_price_db__range=(400, 499.99))

        if color_filter:
            queryset = queryset.filter(color=color_filter)

        if size_filter:
            queryset = queryset.filter(size=size_filter)

        # Apply sorting based on selected option
        if sort_filter == 'latest':
            queryset = queryset.order_by('-created_at')
        elif sort_filter == 'reviews':
            queryset = queryset.annotate(review_count=Count('reviewrating')).order_by('-review_count')
        elif sort_filter == 'rating':
            queryset = queryset.annotate(average_rating=Avg('reviewrating__rating')).order_by('-average_rating')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Product.objects.all()

        # Calculate the counters for each price range
        price_ranges = [
            {'label': '$0 - $99.99', 'value': 'price-1', 'count': self.get_queryset().filter(discounted_price_db__range=(0, 99.99)).count()},
            {'label': '$100 - $199.99', 'value': 'price-2', 'count': self.get_queryset().filter(discounted_price_db__range=(100, 199.99)).count()},
            {'label': '$200 - $299.99', 'value': 'price-3', 'count': self.get_queryset().filter(discounted_price_db__range=(200, 299.99)).count()},
            {'label': '$300 - $399.99', 'value': 'price-4', 'count': self.get_queryset().filter(discounted_price_db__range=(300, 399.99)).count()},
            {'label': '$400 - $499.99', 'value': 'price-5', 'count': self.get_queryset().filter(discounted_price_db__range=(400, 499.99)).count()},
        ]

        context['price_ranges'] = price_ranges
        context['all_products'] = all_products
        # ... other context data ...

        return context


class ProductDetailView(ProductsMixin, CategoryGenderBaseView, DetailView):
    def get(self, request, category_slug, gender_slug, slug):
        product = Product.objects.get(slug=slug)
        if request.user.is_authenticated:
            in_cart = CartItem.objects.filter(cart__user=request.user, product=product).exists()
        else:
            # Handle the case when the user is not logged in
            in_cart = False

        if request.user.is_authenticated:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=product.id).exists()
        else:
            orderproduct = None

        # Get the reviews
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

        # Get the product gallery

        product_gallery = ProductGallery.objects.filter(product_id=product.id)

        context = {
            'product': product,
            'in_cart': in_cart,
            'orderproduct': orderproduct,
            'reviews': reviews,
            'product_gallery': product_gallery,
        }
        return render(request, 'shop_app/product_detail.html', context)


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


class CollectionListView(CategoryGenderBaseView, ListView):

    def get_queryset(self):
        collection_slug = self.kwargs.get('collection_slug')
        collection = get_object_or_404(Collection, slug=collection_slug)

        return Product.objects.filter(collection=collection)


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


# ProductsMixin
class ProductSearchView(ListView):
    template_name = 'shop_app/shop_by.html'
    model = Product
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(product_name__icontains=query)
        return Product.objects.all()


class SubmitReviewView(View):
    def post(self, request, product_id):
        url = request.META.get('HTTP_REFERER')
        try:
            review = ReviewRating.objects.get(user=request.user, product_id=product_id)
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you! Your review has been updated.')
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user = request.user
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')

        return redirect(url)

# def filtered_products(request):
#     selected_ranges = request.GET.getlist('price')

#     price_ranges = {
#         'price-all': (0, 1000),
#         'price-1': (0, 100),
#         'price-2': (100, 200),
#         'price-3': (200, 300),
#         'price-4': (300, 400),
#         'price-5': (400, 500),
#     }

#     filtered_products = Product.objects.all()

#     for selected_range in selected_ranges:
#         min_price, max_price = price_ranges[selected_range]
#         filtered_products = filtered_products.filter(price__gte=min_price, price__lt=max_price)

#     context = {
#         'filtered_products': filtered_products,
#     }

#     return render(request, 'shop_app/shop.html', context)
