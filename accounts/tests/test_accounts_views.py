from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import Account

class TestCustomLoginView(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.user = Account.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_login_success(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('accounts:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
