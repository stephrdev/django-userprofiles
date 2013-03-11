from django.test import TestCase
from django.test.utils import override_settings

from userprofiles.forms import RegistrationForm


class RegistrationFormTests(TestCase):
    """ Test Registration Form against settings """

    def test_email_repeat_disabled(self):
        form_without = RegistrationForm()
        self.assertFalse('email_repeat' in form_without.fields.keys())

    @override_settings(USERPROFILES_DOUBLE_CHECK_EMAIL=True)
    def test_email_repeat_enabled(self):
        form_with = RegistrationForm()
        self.assertTrue('email_repeat' in form_with.fields.keys())

    def test_password_repeat_disabled(self):
        form_without = RegistrationForm()
        self.assertFalse('password_repeat' in form_without.fields.keys())

    @override_settings(USERPROFILES_DOUBLE_CHECK_PASSWORD=True)
    def test_password_repeat_enabled(self):
        form_with = RegistrationForm()
        self.assertTrue('password_repeat' in form_with.fields.keys())

    def test_fullname_disabled(self):
        form_without = RegistrationForm()
        self.assertFalse('first_name' in form_without.fields.keys())
        self.assertFalse('last_name' in form_without.fields.keys())

    @override_settings(USERPROFILES_REGISTRATION_FULLNAME=True)
    def test_fullname_enabled(self):
        form_with = RegistrationForm()
        self.assertTrue('first_name' in form_with.fields.keys())
        self.assertTrue('last_name' in form_with.fields.keys())
