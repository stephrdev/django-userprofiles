from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from userprofiles import settings as up_settings

class SimpleViewTests(TestCase):

    def setUp(self):
        self.data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'email_repeat': 'newuser@example.com',
            'password': 'newuserpass',
            'password_repeat': 'newuserpass',
            'first_name': 'New',
            'last_name': 'User',
        }

    def test_registration(self):
        url = reverse('userprofiles_registration')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse(up_settings.REGISTRATION_REDIRECT))
        self.assertTrue(User.objects.get(username='newuser'))

    def test_email_only_registration(self):
        up_settings.EMAIL_ONLY = True

        url = reverse('userprofiles_registration')
        response = self.client.get(url)
        self.assertTrue('<input type="hidden" name="username"' in response.content)

        data = self.data
        data['username'] = ''

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse(up_settings.REGISTRATION_REDIRECT))
        user = User.objects.get(email=data['email'])
        self.assertNotEqual(user.username, self.data['username'])

        up_settings.EMAIL_ONLY = False

    def test_auto_login(self):
        up_settings.AUTO_LOGIN = True

        url = reverse('userprofiles_registration')
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse(up_settings.REGISTRATION_REDIRECT))

        user = User.objects.get(username=self.data['username'])
        self.assertTrue(user.is_authenticated())

        up_settings.AUTO_LOGIN = False

    def test_email_and_auto_login(self):
        up_settings.EMAIL_ONLY = True
        up_settings.AUTO_LOGIN = True

        url = reverse('userprofiles_registration')
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse(up_settings.REGISTRATION_REDIRECT))

        user = User.objects.get(email=self.data['email'])
        self.assertTrue(user.is_authenticated())

        up_settings.EMAIL_ONLY = False
        up_settings.AUTO_LOGIN = False

    def test_registration_complete(self):
        """ Simple test to make sure this renders """
        response = self.client.get(reverse('userprofiles_registration_complete'))
        self.assertEqual(response.status_code, 200)
