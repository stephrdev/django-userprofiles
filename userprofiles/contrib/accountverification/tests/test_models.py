from datetime import timedelta
from django.test import TestCase
from userprofiles.contrib.accountverification.models import AccountVerification
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

    def test_activation(self):
        user = AccountVerification.objects.create_inactive_user(
            self.data['username'], self.data['password'], self.data['email'])
        user.date_joined = user.date_joined - timedelta(days=up_settings.ACCOUNT_VERIFICATION_DAYS + 1)
        user.save()
        verification = AccountVerification.objects.get(user=user)

        self.assertFalse(
            AccountVerification.objects.activate_user('wrong-pattern-format'))

        self.assertFalse(
            AccountVerification.objects.activate_user('f4a80274f851cb41ef9c20d00426d72fc4874471'))

        self.assertFalse(
            AccountVerification.objects.activate_user(verification.activation_key))

    def test_delete_expired_users(self):
        user = AccountVerification.objects.create_inactive_user(
            self.data['username'], self.data['password'], self.data['email'])

        user.is_active = True
        user.save()
        AccountVerification.objects.delete_expired_users()

        user.date_joined = user.date_joined - timedelta(days=up_settings.ACCOUNT_VERIFICATION_DAYS + 1)
        user.save()
        AccountVerification.objects.delete_expired_users()
        self.assertTrue(AccountVerification.objects.all().exists())

        user.is_active = False
        user.save()
        AccountVerification.objects.delete_expired_users()
        self.assertFalse(AccountVerification.objects.all().exists())

    def test_unicode(self):
        user = AccountVerification.objects.create_inactive_user(
            self.data['username'], self.data['password'], self.data['email'])
        self.assertEqual(
            AccountVerification.objects.get(user=user).__unicode__(),
            'Account verification: %s' % user.username)
