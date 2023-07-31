from django.db import models


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
    discounted_price = models.IntegerField()
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

    def __str__(self):
        return self.product_name

    @property
    def discounted_price(self):
        discounted_price = self.price - self.price * (self.discount_percentage / 100)
        return discounted_price


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

# ToDo Review Rating and Products Gallery
