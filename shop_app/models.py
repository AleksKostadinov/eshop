from django.db import models
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count


class Gender(models.Model):
    gender_name = models.CharField(max_length=10, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    gender_image = models.ImageField(
        upload_to='photos/genders/', blank=True, null=True)
    categories = models.ManyToManyField('Category', blank=True, related_name='gender_categories')

    def __str__(self):
        return self.gender_name


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    category_image = models.ImageField(
        upload_to='photos/categories/', blank=True, null=True)

    # Use ManyToManyField to link to the Gender model with a custom related_name
    genders = models.ManyToManyField(Gender, blank=True, related_name='category_genders')

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    price = models.IntegerField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discounted_price_db = models.IntegerField()
    images = models.ImageField(
        upload_to='photos/products', blank=True, null=True, default='no-products-found.png')
    quantity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def get_url(self):
        return reverse('shop_app:product_detail', args=[self.gender.slug, self.category.slug, self.slug])

    def average_review(self):
        reviews = ReviewRating.objects.filter(
            product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average']:
            avg = float(reviews['average'])
        return avg

    def count_review(self):
        reviews = ReviewRating.objects.filter(
            product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count']:
            count = int(reviews['count'])
        return count

    def __str__(self):
        return self.product_name

    @property
    def discounted_price(self):
        return self.price - self.price * (self.discount_percentage / 100)

    def save(self, *args, **kwargs):
        self.discounted_price_db = self.discounted_price

        super().save(*args, **kwargs)


class VariationManager(models.Manager):
    def colors(self):
        return super().filter(variation_category='color', is_active=True)
    def sizes(self):
        return super().filter(variation_category='size', is_active=True)

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=50, choices=variation_category_choice)
    variation_value = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shop_app/products', max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'Product Gallery'
        verbose_name_plural = 'Product Galleries'
