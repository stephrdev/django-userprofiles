from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from userprofiles.contrib.accountverification.models import AccountVerification
from django.core import mail

import re


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

    @override_settings(USE_ACCOUNT_VERIFICATION=True)
    def test_registration_activate(self):
        AccountVerification.objects.create_inactive_user(
            username=self.data['username'],
            password=self.data['password'],
            email=self.data['email'])
        mailbody = mail.outbox[0].body

        activation_key = re.findall(
            r'http://example.com/userprofiles/activate/(\w+)', mailbody, re.MULTILINE)[0]

        url = reverse('userprofiles_registration_activate',
                      kwargs={'activation_key': activation_key})
        response = self.client.get(url)
        self.assertTrue(
            'We activated your account. You are now able to log in. Have fun!' in
            response.content)
