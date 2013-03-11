from django.conf import settings
from django.contrib.auth.models import SiteProfileNotAvailable
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model
from django.test import TestCase
from django.test.utils import override_settings

from userprofiles import forms
from userprofiles import utils


class UtilsTests(TestCase):
    def test_get_profile_module_disabled(self):
        self.assertEqual(utils.get_profile_model(), None)

    @override_settings(USERPROFILES_USE_PROFILE=True)
    def test_get_profile_module_enabled(self):
        settings.AUTH_PROFILE_MODULE = None
        self.assertRaises(SiteProfileNotAvailable, utils.get_profile_model)

        settings.AUTH_PROFILE_MODULE = 'test_project.test_accounts.Profile'
        self.assertRaises(SiteProfileNotAvailable, utils.get_profile_model)

        settings.AUTH_PROFILE_MODULE = 'test_accounts.InvalidProfile'
        self.assertRaises(SiteProfileNotAvailable, utils.get_profile_model)

        settings.AUTH_PROFILE_MODULE = 'test_accounts.Profile'
        self.assertEqual(utils.get_profile_model(), get_model('test_accounts', 'Profile'))

    def test_get_form_class(self):
        self.assertEqual(utils.get_form_class('userprofiles.forms.RegistrationForm'),
            forms.RegistrationForm)

        self.assertRaises(ImproperlyConfigured,
            utils.get_form_class, 'userprofiles.invalid_forms.RegistrationForm')

        self.assertRaises(ImproperlyConfigured,
            utils.get_form_class, 'userprofiles.forms.InvalidRegistrationForm')
