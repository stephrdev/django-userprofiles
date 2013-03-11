from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from userprofiles.contrib.emailverification.models import EmailVerification
from userprofiles.settings import up_settings


@override_settings(USERPROFILES_USE_PROFILE=False, USERPROFILES_USE_EMAIL_VERIFICATION=True)
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

        self.user = User.objects.create_user(self.data['username'],
            self.data['email'], self.data['password'])

    def tearDown(self):
        self.user.delete()

    def test_email_change(self):
        self.client.login(username=self.data['username'], password=self.data['password'])

        response = self.client.get(reverse('userprofiles_email_change'))

        response = self.client.post(reverse('userprofiles_email_change'),
            {'new_email': 'test@example.com'}, follow=True)

        self.assertTrue(EmailVerification.objects.filter(user=self.user).exists())

        self.assertEqual(response.context['expiration_days'], up_settings.EMAIL_VERIFICATION_DAYS)

    def test_email_change_email_in_use(self):
        EmailVerification.objects.create(
            user=self.user, old_email=self.user.email, new_email='test@example.com')

        self.client.login(username=self.data['username'], password=self.data['password'])

        response = self.client.post(reverse('userprofiles_email_change'),
            {'new_email': 'test@example.com'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'new_email',
            [u'This email address is already in use. Please supply a different email address.'])

    def test_email_change_approve(self):
        verification = EmailVerification.objects.create(
            user=self.user, old_email=self.user.email, new_email='test@example.com')

        self.client.login(username=self.data['username'], password=self.data['password'])

        url = reverse('userprofiles_email_change_approve',
            kwargs={'token': verification.token, 'code': verification.code})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.get(pk=self.user.pk).email, 'test@example.com')

        self.assertFalse(EmailVerification.objects.filter(user=self.user,
            is_approved=False).exists())

    def test_email_change_approve_not_exists(self):
        verification = EmailVerification.objects.create(
            user=self.user, old_email=self.user.email, new_email='test@example.com')

        self.client.login(username=self.data['username'], password=self.data['password'])

        url = reverse('userprofiles_email_change_approve',
            kwargs={'token': verification.token, 'code': 'wrong-code'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.get(pk=self.user.pk).email, self.user.email)

        url = reverse('userprofiles_email_change_approve',
            kwargs={'token': 'wrong-token', 'code': verification.code})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.get(pk=self.user.pk).email, self.user.email)
