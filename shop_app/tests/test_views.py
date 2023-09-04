from accounts.models import Account
from django.test import Client, TestCase
from django.urls import reverse

from shop_app.models import Category, Gender, Product


class TestShopappViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(category_name='Test Category', slug='test-category')
        self.gender = Gender.objects.create(gender_name='Test Gender', slug='test-gender')
        self.product = Product.objects.create(product_name='Test Product', slug='test-product', category=self.category, gender=self.gender)
        self.user = Account.objects.create_user(username='testuser', password='testpassword')
        self.product1 = Product.objects.create(product_name='Test Product 1', slug='test-product-1', category=self.category, gender=self.gender)
        self.product2 = Product.objects.create(product_name='Test Product 2', slug='test-product-2', category=self.category, gender=self.gender)

    def test_category_gender_base_view(self):
        response = self.client.get(reverse('shop_app:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop_app/home.html')
        self.assertContains(response, 'Test Category')
        self.assertContains(response, 'Test Gender')

    def test_home_list_view(self):
        response = self.client.get(reverse('shop_app:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop_app/home.html')
        self.assertContains(response, 'Test Product')

    def test_product_detail_view(self):
        response = self.client.get(reverse('shop_app:product_detail', kwargs={'category_slug': self.category.slug, 'gender_slug': self.gender.slug, 'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop_app/product_detail.html')

    def test_product_search_view(self):
        response = self.client.get(reverse('shop_app:product_search'), {'q': 'Test Product 1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop_app/shop.html')
        self.assertContains(response, 'Test Product 1')
        self.assertNotContains(response, 'Test Product 2')
