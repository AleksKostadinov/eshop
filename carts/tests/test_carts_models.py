from django.test import TestCase
from django.urls import reverse
from accounts.models import Account
from shop_app.models import (Cover, Product, Gender, Category,
                             Collection, Variation, ReviewRating, ProductGallery)
from django.utils import timezone


class TestGenderModel(TestCase):
    def setUp(self):
        self.gender = Gender.objects.create(
            gender_name='Test Gender', slug='test-gender', description='Test Description')

    def test_gender_str(self):
        self.assertEqual(str(self.gender), 'Test Gender')


class TestCategoryModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            category_name='Test Category', slug='test-category', description='Test Description')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Test Category')


class TestCoverModel(TestCase):
    def setUp(self):
        self.cover = Cover.objects.create(
            cover_name='Test Cover', slug='test-cover', cover_title='Test Title', description='Test Description')

    def test_cover_str(self):
        self.assertEqual(str(self.cover), 'Test Cover')


class TestProductModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            category_name='Test Category', slug='test-category')
        self.gender = Gender.objects.create(
            gender_name='Test Gender', slug='test-gender')
        self.collection = Collection.objects.create(
            collection_name='Test Collection', slug='test-collection',
            start_date=timezone.now().date(), end_date=timezone.now().date() + timezone.timedelta(days=30))

        self.product = Product.objects.create(
            product_name='Test Product', slug='test-product',
            price=10, discounted_price_db=8, quantity=10,
            category=self.category, gender=self.gender,
            collection=self.collection)

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Test Product')

    def test_get_url(self):
        url = self.product.get_url()
        expected_url = reverse('shop_app:product_detail', args=[
            self.gender.slug, self.category.slug, self.product.slug])
        self.assertEqual(url, expected_url)

    def test_collection_in_season(self):
        # Assuming the collection is in season at the current date
        self.assertTrue(self.product.collection_in_season())

    def test_save_method(self):
        self.product.save()


class TestCollectionModel(TestCase):
    def setUp(self):
        self.collection = Collection.objects.create(
            collection_name='Test Collection', slug='test-collection',
            start_date=timezone.now().date(), end_date=timezone.now().date() + timezone.timedelta(days=30))

    def test_collection_str(self):
        self.assertEqual(str(self.collection), 'Test Collection')


class TestVariationModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            category_name='Test Category', slug='test-category')
        self.gender = Gender.objects.create(
            gender_name='Test Gender', slug='test-gender')
        self.product = Product.objects.create(
            product_name='Test Product', slug='test-product',
            price=10, discounted_price_db=8, quantity=10,
            category=self.category, gender=self.gender)
        self.variation = Variation.objects.create(
            product=self.product, variation_category='color', variation_value='Red')

    def test_variation_str(self):
        self.assertEqual(str(self.variation), 'Red')


class TestReviewRatingModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            category_name='Test Category', slug='test-category')
        self.gender = Gender.objects.create(
            gender_name='Test Gender', slug='test-gender')
        self.product = Product.objects.create(
            product_name='Test Product', slug='test-product',
            price=10, discounted_price_db=8, quantity=10,
            category=self.category, gender=self.gender)
        self.user = Account.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword')
        self.review = ReviewRating.objects.create(
            product=self.product, user=self.user,
            subject='Test Subject', review='Test Review',
            rating=5, ip='127.0.0.1')

    def test_review_rating_str(self):
        self.assertEqual(str(self.review), 'Test Subject')


class TestProductGalleryModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            category_name='Test Category', slug='test-category')
        self.gender = Gender.objects.create(
            gender_name='Test Gender', slug='test-gender')
        self.product = Product.objects.create(
            product_name='Test Product', slug='test-product',
            price=10, discounted_price_db=8, quantity=10,
            category=self.category, gender=self.gender)
        self.product_gallery = ProductGallery.objects.create(
            product=self.product, image='test.jpg')

    def test_product_gallery_str(self):
        self.assertEqual(str(self.product_gallery), 'Test Product')
