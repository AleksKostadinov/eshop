from django.test import TestCase
from accounts.models import Account
from shop_app.models import Product
from orders.models import ShippingConfig, Payment, Order, OrderProduct

class ShippingConfigModelTest(TestCase):
    def test_shipping_config_str(self):
        shipping_config = ShippingConfig.objects.create(shipping_cost_percent=5.0)
        self.assertEqual(str(shipping_config), 'Shipping Percent: 5.0')

class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword')

    def test_payment_str(self):
        payment = Payment.objects.create(
            user=self.user, payment_id='12345', payment_method='Credit Card',
            amount_paid='50.00', status='Paid')
        self.assertEqual(str(payment), '12345')

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword')

    def test_order_str(self):
        order = Order.objects.create(
            user=self.user, order_number='12345', first_name='John', last_name='Doe',
            phone='1234567890', email='john@example.com', address_line_1='123 Main St',
            country='US', state='CA', city='Los Angeles', order_total=50.00, tax=5.00)
        self.assertEqual(str(order), 'John')


class OrderProductModelTest(TestCase):
    def setUp(self):
        # Create necessary objects like Account, Product, etc.
        self.user = Account.objects.create(username='testuser', email='test@example.com', password='testpassword')
        self.product = Product.objects.create(
            product_name='Test Product',
            price=10,
            discounted_price_db=8,
            quantity=10,
            category=None,
            gender=None
        )
        self.order = Order.objects.create(
            user=self.user,
            order_number='123456',
            first_name='John',
            last_name='Doe',
            phone='1234567890',
            email='john@example.com',
            address_line_1='123 Main St',
            country='US',
            state='CA',
            city='Los Angeles',
            order_total=10.00,
            tax=1.00,
            status='New',
            ip='127.0.0.1',
            is_ordered=False
        )

    def test_order_product_creation(self):
        order_product = OrderProduct.objects.create(
            order=self.order,  # Provide the order here
            user=self.user,
            product_name='Test Product',
            product_price=10.00,
            quantity=2,
            product_image=None,
            product=self.product
        )
        self.assertEqual(str(order_product), 'Test Product')

