from django.test import TestCase

from userprofiles.forms import RegistrationForm
from userprofiles import settings as up_settings


class RegistrationFormTests(TestCase):
    """ Test Registration Form against settings """

    def test_email_repeat(self):
        form_without = RegistrationForm()
        self.assertFalse('email_repeat' in form_without.fields.keys())

        up_settings.DOUBLE_CHECK_EMAIL = True
        form_with = RegistrationForm()
        self.assertTrue('email_repeat' in form_with.fields.keys())
        up_settings.DOUBLE_CHECK_EMAIL = False

    def test_password_repeat(self):
        form_without = RegistrationForm()
        self.assertFalse('password_repeat' in form_without.fields.keys())

        up_settings.DOUBLE_CHECK_PASSWORD = True
        form_with = RegistrationForm()
        self.assertTrue('password_repeat' in form_with.fields.keys())
        up_settings.DOUBLE_CHECK_PASSWORD = False

    def test_fullname(self):
        form_without = RegistrationForm()
        self.assertFalse('first_name' in form_without.fields.keys())
        self.assertFalse('last_name' in form_without.fields.keys())

        up_settings.REGISTRATION_FULLNAME = True
        form_with = RegistrationForm()
        self.assertTrue('first_name' in form_with.fields.keys())
        self.assertTrue('last_name' in form_with.fields.keys())
        up_settings.REGISTRATION_FULLNAME = False
