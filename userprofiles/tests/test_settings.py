from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.test.utils import override_settings

from userprofiles.settings import validate_settings


class SettingsTests(TestCase):
    @override_settings(USERPROFILES_USE_ACCOUNT_VERIFICATION=True,
        INSTALLED_APPS=list(set(settings.INSTALLED_APPS) - set(
            ['userprofiles.contrib.accountverification'])))
    def test_account_verification(self):
        self.assertRaises(ImproperlyConfigured, validate_settings)

    @override_settings(USERPROFILES_USE_ACCOUNT_VERIFICATION=True,
        USERPROFILES_AUTO_LOGIN=True)
    def test_account_verification_auto_login(self):
        self.assertRaises(ImproperlyConfigured, validate_settings)

    @override_settings(USERPROFILES_USE_PROFILE=True,
        INSTALLED_APPS=list(set(settings.INSTALLED_APPS) - set(
            ['userprofiles.contrib.profiles'])))
    def test_profile(self):
        self.assertRaises(ImproperlyConfigured, validate_settings)

    @override_settings(USERPROFILES_PROFILE_ALLOW_EMAIL_CHANGE=True,
        USERPROFILES_CHECK_UNIQUE_EMAIL=True)
    def test_profile_email_check(self):
        self.assertRaises(ImproperlyConfigured, validate_settings)

    @override_settings(USERPROFILES_USE_EMAIL_VERIFICATION=True,
        INSTALLED_APPS=list(set(settings.INSTALLED_APPS) - set(
            ['userprofiles.contrib.emailverification'])))
    def test_email_verification(self):
        self.assertRaises(ImproperlyConfigured, validate_settings)

    @override_settings(USERPROFILES_USE_EMAIL_VERIFICATION=True,
        USERPROFILES_PROFILE_ALLOW_EMAIL_CHANGE=True)
    def test_email_verification_allow_email_change(self):
        self.assertRaises(ImproperlyConfigured, validate_settings)
