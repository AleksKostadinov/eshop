from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from unittest.mock import patch
from django.utils import timezone
from accounts.models import Account
from shop_app.models import Category
from shop_app.models import Gender
from shop_app.models import Collection
from shop_app.models import Product
from shop_app.models import ReviewRating


class ProductModelTestCase(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            username='testuser', password='testpassword')
        self.category = Category.objects.create(category_name='Test Category', slug='test-category')
        self.gender = Gender.objects.create(gender_name='Test Gender', slug='test-gender')
        self.collection = Collection.objects.create(
            collection_name='Test Collection',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=7),
            additional_discount_percentage=10
        )
        self.product = Product.objects.create(
            product_name='Test Product',
            slug='test-product',
            description='Test description',
            price=100,
            discount_percentage=20,
            quantity=10,
            category=self.category,
            gender=self.gender,
            collection=self.collection,
        )
        self.product.users_wishlist.add(self.user)

    def test_get_url(self):
        url = self.product.get_url()
        expected_url = reverse(
            'shop_app:product_detail',
            args=[self.gender.slug, self.category.slug, self.product.slug]
        )
        self.assertEqual(url, expected_url)

    def test_average_review_with_reviews(self):
        ReviewRating.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            status=True
        )
        ReviewRating.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            status=True
        )
        avg_rating = self.product.average_review()
        self.assertEqual(avg_rating, 4.5)

    def test_average_review_without_reviews(self):
        avg_rating = self.product.average_review()
        self.assertEqual(avg_rating, 0)

    def test_count_review_with_reviews(self):
        ReviewRating.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            status=True
        )
        ReviewRating.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            status=True
        )
        review_count = self.product.count_review()
        self.assertEqual(review_count, 2)

    def test_count_review_without_reviews(self):
        review_count = self.product.count_review()
        self.assertEqual(review_count, 0)

    def test_discounted_price_with_collection(self):
        self.assertEqual(self.product.discounted_price, Decimal('72.00'))

    def test_discounted_price_without_collection(self):
        self.product.collection = None
        self.product.save()
        self.assertEqual(self.product.discounted_price, Decimal('80.00'))

    def test_collection_in_season_true(self):
        with patch.object(timezone, 'now', return_value=timezone.now()):
            self.assertTrue(self.product.collection_in_season())

    def test_collection_in_season_false(self):
        with patch.object(timezone, 'now', return_value=timezone.now() + timezone.timedelta(days=10)):
            self.assertFalse(self.product.collection_in_season())

    def test_save_additional_discount_percentage_with_collection_in_season(self):
        self.product.save()
        self.assertEqual(self.product.additional_discount_percentage, Decimal('10.00'))

    def test_save_additional_discount_percentage_without_collection_in_season(self):
        self.product.collection = None
        self.product.save()
        self.assertEqual(self.product.additional_discount_percentage, Decimal('0.00'))

    def test_save_discounted_price_db(self):
        self.product.save()
        self.assertEqual(self.product.discounted_price_db, Decimal('72.00'))

    def test_save_with_collection(self):
        self.assertEqual(self.product.additional_discount_percentage, Decimal('10.00'))
        self.assertEqual(self.product.discounted_price_db, Decimal('72.00'))

    def test_save_without_collection(self):
        self.product.collection = None
        self.product.save()
        self.assertEqual(self.product.additional_discount_percentage, Decimal('0.00'))
        self.assertEqual(self.product.discounted_price_db, Decimal('80.00'))
