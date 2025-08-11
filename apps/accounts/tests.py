from django.test import TestCase, override_settings
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
import datetime

from .models import User


@override_settings(PASSWORD_HASHERS=("django.contrib.auth.hashers.MD5PasswordHasher",))
class UserModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create_user(
            email='testemail@gmail.com',
            password='testpassword',
            first_name='test',
            last_name='user',
        )

    def test_user_model(self):
        self.assertEqual(self.user.email, 'testemail@gmail.com')
        self.assertTrue(self.user.check_password('testpassword'))
        self.assertIsNotNone(self.user.profile, msg='Test that the profile was created automatically')
        self.assertEqual(self.user.get_full_name(), 'Test User')

    def test_default_fields(self):
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(self.user.is_superuser, False)
    
    def test_user_instances(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(settings.AUTH_USER_MODEL, 'accounts.User')


@override_settings(PASSWORD_HASHERS=("django.contrib.auth.hashers.MD5PasswordHasher",))
class UserAPITest(TestCase):
    pass


