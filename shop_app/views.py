from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from accounts.models import SubscribedUsers
from carts.models import CartItem
from core.views_mixins import ProductFilterMixin
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
from django.db.models import Count
from django.contrib.auth.mixins import UserPassesTestMixin


def custom_404(request, exception):
    error_message = "Page Not Found"
    return render(request, '404.html', {'error_message': error_message}, status=404)


def custom_500(request, exception):
    error_message = str(exception) if exception else "Internal Server Error"
    return render(request, '500.html', {'error_message': error_message}, status=500)


class CategoryGenderBaseView(ProductFilterMixin):
    template_name = 'shop_app/shop.html'
    context_object_name = 'products'
    paginate_by = 8

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
        context['just_arrived'] = self.model.objects.order_by('-created_at')[:6]
        return context


class ShopListView(CategoryGenderBaseView, ListView):
    template_name = 'shop_app/shop.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ProductDetailView(CategoryGenderBaseView, DetailView):
    def get(self, request, category_slug, gender_slug, slug):
        product = Product.objects.get(slug=slug)
        products = Product.objects.filter(gender__slug=gender_slug)
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
            'products': products,
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
