from django.contrib.auth.models import User
from django.test import TestCase
from django.test.utils import override_settings

from userprofiles.contrib.accountverification.models import AccountVerification
from userprofiles.contrib.emailverification.models import EmailVerification
from userprofiles.forms import RegistrationForm


class RegistrationFormTests(TestCase):
    """ Test Registration Form against settings """

    def setUp(self):
        self.existing_user = User.objects.create(username='existinguser',
            email='existingemail@example.com')

    def tearDown(self):
        self.existing_user.delete()

    def test_email_repeat_disabled(self):
        form = RegistrationForm()
        self.assertFalse('email_repeat' in form.fields.keys())

    @override_settings(USERPROFILES_DOUBLE_CHECK_EMAIL=True)
    def test_email_repeat_enabled(self):
        form = RegistrationForm()
        self.assertTrue('email_repeat' in form.fields.keys())

    def test_password_repeat_disabled(self):
        form = RegistrationForm()
        self.assertFalse('password_repeat' in form.fields.keys())

    @override_settings(USERPROFILES_DOUBLE_CHECK_PASSWORD=True)
    def test_password_repeat_enabled(self):
        form = RegistrationForm()
        self.assertTrue('password_repeat' in form.fields.keys())

    def test_fullname_disabled(self):
        form = RegistrationForm()
        self.assertFalse('first_name' in form.fields.keys())
        self.assertFalse('last_name' in form.fields.keys())

    @override_settings(USERPROFILES_REGISTRATION_FULLNAME=True)
    def test_fullname_enabled(self):
        form = RegistrationForm()
        self.assertTrue('first_name' in form.fields.keys())
        self.assertTrue('last_name' in form.fields.keys())

    def test_clean_username_email_only_disabled(self):
        form = RegistrationForm({
            'username': 'test',
            'email': 'test@example.com',
            'password': 'password'
        })
        self.assertTrue(form.is_valid())

        form = RegistrationForm({
            'username': 'existinguser',
            'email': 'test@example.com',
            'password': 'password'
        })
        self.assertFalse(form.is_valid())

    def test_clean_email_unique_disabled(self):
        form = RegistrationForm({
            'username': 'test',
            'email': 'existingemail@example.com',
            'password': 'password'
        })
        self.assertTrue(form.is_valid())

    @override_settings(USERPROFILES_CHECK_UNIQUE_EMAIL=True)
    def test_clean_email_unique_enabled(self):
        form = RegistrationForm({
            'username': 'test',
            'email': 'test@example.com',
            'password': 'password'
        })
        self.assertTrue(form.is_valid())

        form = RegistrationForm({
            'username': 'test',
            'email': 'existingemail@example.com',
            'password': 'password'
        })
        self.assertFalse(form.is_valid())

    @override_settings(USERPROFILES_CHECK_UNIQUE_EMAIL=True,
        USERPROFILES_USE_EMAIL_VERIFICATION=True)
    def test_clean_email_unique_enabled_with_emailverification(self):
        form = RegistrationForm({
            'username': 'test',
            'email': 'existingemail2@example.com',
            'password': 'password'
        })
        self.assertTrue(form.is_valid())

        EmailVerification.objects.create(user=self.existing_user,
            old_email=self.existing_user.email, new_email='existingemail2@example.com')

        form = RegistrationForm({
            'username': 'test',
            'email': 'existingemail2@example.com',
            'password': 'password'
        })
        self.assertFalse(form.is_valid())

    @override_settings(USERPROFILES_DOUBLE_CHECK_EMAIL=True)
    def test_double_check_email(self):
        form = RegistrationForm({
            'username': 'test',
            'email': 'test@example.com',
            'email_repeat': 'test@example.com',
            'password': 'password'
        })
        self.assertTrue(form.is_valid())

        form = RegistrationForm({
            'username': 'test',
            'email': 'test@example.com',
            'email_repeat': 'test2@example.com',
            'password': 'password'
        })
        self.assertFalse(form.is_valid())

    @override_settings(USERPROFILES_DOUBLE_CHECK_PASSWORD=True)
    def test_double_check_password(self):
        form = RegistrationForm({
            'username': 'test',
            'email': 'test@example.com',
            'password': 'password',
            'password_repeat': 'password'
        })
        self.assertTrue(form.is_valid())

        form = RegistrationForm({
            'username': 'test',
            'email': 'test@example.com',
            'password': 'password',
            'password_repeat': 'password2'
        })
        self.assertFalse(form.is_valid())

    def test_form_save(self):
        form = RegistrationForm({
            'username': 'test',
            'email': 'test@example.com',
            'password': 'password'
        })
        self.assertTrue(form.is_valid())
        new_user = form.save()

        self.assertEqual(new_user.username, 'test')
        self.assertTrue(new_user.is_active)

    @override_settings(USERPROFILES_USE_ACCOUNT_VERIFICATION=True)
    def test_form_save_with_account_verification(self):
        form = RegistrationForm({
            'username': 'test',
            'email': 'test@example.com',
            'password': 'password'
        })
        self.assertTrue(form.is_valid())
        new_user = form.save()

        self.assertEqual(new_user.username, 'test')
        self.assertFalse(new_user.is_active)

        self.assertEqual(AccountVerification.objects.count(), 1)

    @override_settings(USERPROFILES_REGISTRATION_FULLNAME=True)
    def test_form_save_with_fullname(self):
        form = RegistrationForm({
            'username': 'test',
            'email': 'test@example.com',
            'password': 'password',
            'first_name': 'First',
            'last_name': 'Last',
        })
        self.assertTrue(form.is_valid())
        new_user = form.save()

        self.assertEqual(new_user.username, 'test')
        self.assertTrue(new_user.is_active)

        self.assertEqual(new_user.first_name, 'First')
        self.assertEqual(new_user.last_name, 'Last')
