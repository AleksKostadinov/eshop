# from django.test import TestCase
# from django.utils import timezone
# from accounts.models import Account, SubscribedUsers


# class TestAccountModel(TestCase):
#     def setUp(self):
#         self.user = Account.objects.create(
#             first_name='John',
#             last_name='Doe',
#             email='johndoe@example.com',
#             phone_number='1234567890'
#         )

#     def test_full_name(self):
#         self.assertEqual(self.user.full_name(), 'John Doe')

#     def test_full_name_with_empty_last_name(self):
#         self.user.last_name = ''
#         self.assertEqual(self.user.full_name(), 'John ')

#     def test_full_name_with_empty_first_name(self):
#         self.user.first_name = ''
#         self.assertEqual(self.user.full_name(), ' Doe')


# class TestSubscribedUsersModel(TestCase):
#     def test_subscribed_users_model(self):
#             subscribed_user = SubscribedUsers.objects.create(
#                 name='Jane Doe',
#                 email='janedoe@example.com'
#             )
#             self.assertEqual(str(subscribed_user), 'janedoe@example.com')
#             self.assertEqual(subscribed_user.created_date.date(), timezone.now().date())

#     def test_subscribed_users_model_with_duplicate_email(self):
#         SubscribedUsers.objects.create(
#             name='John Doe',
#             email='johndoe@example.com'
#         )
#         with self.assertRaises(Exception):
#             SubscribedUsers.objects.create(
#                 name='Jane Doe',
#                 email='johndoe@example.com'
#             )
