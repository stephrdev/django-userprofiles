from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.utils import override_settings


class AuthBackendTests(TestCase):
    def setUp(self):
        self.existing_user = User.objects.create_user(username='test',
            email='test@example.com', password='password')

    def tearDown(self):
        self.existing_user.delete()

    def test_without_email_auth_backend(self):
        user = authenticate(username='test2', password='password2')
        self.assertEqual(user, None)

        user = authenticate(username='test', password='password')
        self.assertEqual(user, self.existing_user)

        user = authenticate(username='test@example.com', password='password')
        self.assertEqual(user, None)

    @override_settings(AUTHENTICATION_BACKENDS=[
        'userprofiles.auth_backends.EmailOrUsernameModelBackend'])
    def test_with_email_auth_backend(self):
        user = authenticate(username='test2', password='password2')
        self.assertEqual(user, None)

        user = authenticate(username='test', password='password')
        self.assertEqual(user, self.existing_user)

        user = authenticate(username='test@example.com', password='password')
        self.assertEqual(user, self.existing_user)
