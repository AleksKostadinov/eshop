from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from accounts.models import SubscribedUsers
from carts.models import CartItem
from orders.models import OrderProduct
from shop_app.admin import Brand
from shop_app.forms import ContactForm, NewsletterForm, ReviewForm
from shop_app.models import Collection, Cover, Gender, Product, Category, ProductGallery, ReviewRating, Variation
from django.views.generic import ListView, DetailView, FormView
from django.urls import reverse_lazy
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.db.models import Avg, Count
from django.contrib.auth.mixins import UserPassesTestMixin


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


class ProductFilterMixin:
    price_ranges = {
        'price-1': (0, 99.99),
        'price-2': (100, 199.99),
        'price-3': (200, 299.99),
        'price-4': (300, 399.99),
        'price-5': (400, 499.99),
    }

    def apply_price_filter(self, queryset, price_filter):
        price_range = self.price_ranges.get(price_filter)
        if price_range:
            queryset = queryset.filter(discounted_price_db__range=price_range)
        return queryset

    def apply_variation_filter(self, queryset, filter_value, variation_category):
        if filter_value:
            if filter_value == f'{variation_category}-all':
                pass
            else:
                queryset = queryset.filter(
                    variation__variation_category=variation_category,
                    variation__variation_value=filter_value
                )
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()

        price_filter = self.request.GET.get('price')
        color_filter = self.request.GET.get('color')
        size_filter = self.request.GET.get('size')
        sort_filter = self.request.GET.get('sort')

        queryset = self.apply_price_filter(queryset, price_filter)
        queryset = self.apply_variation_filter(queryset, color_filter, 'color')
        queryset = self.apply_variation_filter(queryset, size_filter, 'size')

        if sort_filter == 'latest':
            queryset = queryset.order_by('-created_at')
        elif sort_filter == 'reviews':
            queryset = queryset.annotate(review_count=Count('reviewrating')).order_by('-review_count')
        elif sort_filter == 'rating':
            queryset = queryset.annotate(average_rating=Avg('reviewrating__rating')).order_by('-average_rating')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_price = self.request.GET.get('price')
        selected_color = self.request.GET.get('color')
        selected_size = self.request.GET.get('size')
        context['selected_price'] = selected_price
        context['selected_color'] = selected_color
        context['selected_size'] = selected_size

        context['available_colors'] = Variation.objects.filter(
            variation_category='color',
            is_active=True
        ).values_list('variation_value', flat=True).distinct()

        context['available_sizes'] = Variation.objects.filter(
            variation_category='size',
            is_active=True
        ).values_list('variation_value', flat=True).distinct()

        context['price_ranges'] = [
            {'label': '$0 - $99.99', 'value': 'price-1'},
            {'label': '$100 - $199.99', 'value': 'price-2'},
            {'label': '$200 - $299.99', 'value': 'price-3'},
            {'label': '$300 - $399.99', 'value': 'price-4'},
            {'label': '$400 - $499.99', 'value': 'price-5'},
        ]

        return context


class CategoryGenderBaseView(ProductFilterMixin):
    template_name = 'shop_app/shop.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        genders = Gender.objects.annotate(product_count=Count('product'))
        collections = Collection.objects.all()
        brands = Brand.objects.all()
        covers = Cover.objects.all()
        context['categories'] = categories
        context['genders'] = genders
        context['collections'] = collections
        context['brands'] = brands
        context['covers'] = covers
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


class ShopListView(CategoryGenderBaseView, ProductFilterMixin, ListView):
    template_name = 'shop_app/shop.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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
class ProductSearchView(CategoryGenderBaseView, ListView):
    template_name = 'shop_app/shop.html'
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


class NewsletterView(UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get(self, request):
        form = NewsletterForm()
        form.fields['receivers'].initial = ', '.join([active.email for active in SubscribedUsers.objects.all()])
        context = {
            'form': form,
            }

        return render(request, 'base/newsletter.html', context)

    def post(self, request):
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            receivers = form.cleaned_data.get('receivers').split(',')
            email_message = form.cleaned_data.get('message')

            mail = EmailMessage(subject, email_message, f"EShop <{request.user.email}>", bcc=receivers)

            mail.content_subtype = 'html'

            if mail.send():
                messages.success(request, "Email sent successfully")
            else:
                messages.error(request, "There was an error sending the email")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

        return redirect('/')
