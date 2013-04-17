from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from userprofiles.settings import up_settings


class ViewTests(TestCase):
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

    @override_settings(USERPROFILES_EMAIL_ONLY=True)
    def test_email_only_registration(self):
        url = reverse('userprofiles_registration')
        response = self.client.get(url)

        self.assertTrue('<input type="hidden" name="username"' in response.content or
            '<input id="id_username" name="username" type="hidden" />' in response.content)

        data = self.data
        data['username'] = ''

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse(up_settings.REGISTRATION_REDIRECT))
        user = User.objects.get(email=data['email'])
        self.assertNotEqual(user.username, self.data['username'])

    @override_settings(USERPROFILES_AUTO_LOGIN=True)
    def test_auto_login(self):
        url = reverse('userprofiles_registration')
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse(up_settings.REGISTRATION_REDIRECT))

        user = User.objects.get(username=self.data['username'])
        self.assertTrue(user.is_authenticated())

    @override_settings(USERPROFILES_AUTO_LOGIN=True, USERPROFILES_EMAIL_ONLY=True)
    def test_email_and_auto_login(self):
        url = reverse('userprofiles_registration')
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse(up_settings.REGISTRATION_REDIRECT))

        user = User.objects.get(email=self.data['email'])
        self.assertTrue(user.is_authenticated())

    def test_registration_complete(self):
        """ Simple test to make sure this renders """
        response = self.client.get(reverse('userprofiles_registration_complete'))
        self.assertEqual(response.status_code, 200)
