from rest_framework.test import APITestCase
from django.contrib.auth.models  import User

class TestModel(APITestCase):

    def test_create_user(self):
        user = User.objects.create(username='test', email='test@test.com', first_name='FTest', last_name='LTest', password='test12345')

        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email, 'test@test.com')

    def test_raises_error_when_no_username_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, username='', email='', password='test12345' )


    def test_raises_error_with_message_when_no_username_is_supplied(self):
        with self.assertRaisesMessage(ValueError, 'The given username must be set'):
            User.objects.create_user(username='', email='test@test.com', password='test12345')
    
    def test_raises_error_when_no_email_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, username="username", email='', password='test12345')

    def test_raises_error_with_message_when_no_email_is_supplied(self):
        with self.assertRaisesMessage(ValueError, 'The given email must be set'):
            User.objects.create_user(
                username='username', email='', password='password123!@')

    def test_cant_create_super_user_with_not_is_staff_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_staff=True.'):
            User.objects.create_superuser(username='test', email='test@test.com', password='test12345', is_staff=False)
    
    def test_cant_create_super_user_with_not_super_user_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_superuser=True.'):
            User.objects.create_superuser(
                username='test', email='test@test.com', password='test12345', is_superuser=False)

    
    def test_creates_super_user(self):
        user = User.objects.create_superuser('test', 'test@test.com', 'test12345')
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.email, 'test@test.com')
