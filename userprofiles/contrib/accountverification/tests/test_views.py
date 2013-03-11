import re

from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from userprofiles.contrib.accountverification.models import AccountVerification


@override_settings(USE_ACCOUNT_VERIFICATION=True)
class ViewTests(TestCase):
    def setUp(self):
        self.data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newuserpass',
        }

    def test_registration_activate(self):
        AccountVerification.objects.create_inactive_user(
            self.data['username'], self.data['password'], self.data['email'])

        self.assertEqual(len(mail.outbox), 1)

        activation_key_match = re.findall(
            r'http://example.com/userprofiles/activate/(\w+)',
            mail.outbox[0].body, re.MULTILINE)

        self.assertEqual(len(activation_key_match), 1)

        activation_key = activation_key_match[0]

        url = reverse('userprofiles_registration_activate',
            kwargs={'activation_key': activation_key})

        response = self.client.get(url)
        self.assertTrue(
            'We activated your account. You are now able to log in. Have fun!' in
            response.content)
