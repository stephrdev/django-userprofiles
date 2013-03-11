from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from userprofiles.contrib.accountverification.models import AccountVerification
from userprofiles.settings import up_settings


class ModelsTests(TestCase):
    def setUp(self):
        self.data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newuserpass',
        }

    def test_activate_user(self):
        user = AccountVerification.objects.create_inactive_user(
            self.data['username'], self.data['password'], self.data['email'])
        user.date_joined = user.date_joined - timedelta(
            days=up_settings.ACCOUNT_VERIFICATION_DAYS, seconds=1)
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

        # Test with inactive user, but not expired
        AccountVerification.objects.delete_expired_users()
        self.assertTrue(User.objects.filter(pk=user.pk).exists())

        # Test with active and not expired user
        user.is_active = True
        user.save()
        AccountVerification.objects.delete_expired_users()
        self.assertTrue(User.objects.filter(pk=user.pk).exists())

        # Test with active but expired user
        user.date_joined = user.date_joined - timedelta(
            days=up_settings.ACCOUNT_VERIFICATION_DAYS + 1)
        user.save()
        AccountVerification.objects.delete_expired_users()
        self.assertTrue(User.objects.filter(pk=user.pk).exists())

        # Test with expired and inactive user
        user.is_active = False
        user.save()
        AccountVerification.objects.delete_expired_users()
        self.assertFalse(User.objects.filter(pk=user.pk).exists())
