from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.utils import override_settings
from django.conf import settings
from test_project.test_accounts.models import Profile


@override_settings(INSTALLED_APPS=settings.INSTALLED_APPS + ['userprofiles.contrib.profiles'])
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
        user = User.objects.create_user(self.data['username'], self.data['email'],
                                        self.data['password'])
        Profile(user=user).save()

    def tearDown(self):
        User.objects.get(username=self.data['username']).delete()

    @override_settings(USERPROFILES_USE_PROFILE=True)
    def test_profile_view(self):
        self.client.login(username=self.data['username'], password=self.data['password'])
        url = reverse('userprofiles_profile')
        response = self.client.get(url)
        self.assertTrue('newuser' in response.content)

    @override_settings(USERPROFILES_USE_PROFILE=True, USERPROFILES_REGISTRATION_FULLNAME=True)
    def test_profile_change_fullname_enabled(self):
        settings.AUTH_PROFILE_MODULE = 'test_accounts.Profile'
        self.client.login(username=self.data['username'], password=self.data['password'])
        url = reverse('userprofiles_profile_change')
        response = self.client.get(url)
        self.assertTrue('first_name' in response.content and
                        'last_name' in response.content)
        self.client.post(url, {'first_name': 'john', 'last_name': 'doe'})
        response = self.client.get(url)
        self.assertTrue('john' in response.content and
                        'doe' in response.content)

    @override_settings(USERPROFILES_USE_PROFILE=True, USERPROFILES_REGISTRATION_FULLNAME=False)
    def test_profile_change_fullname_disabled(self):
        settings.AUTH_PROFILE_MODULE = 'test_accounts.Profile'
        self.client.login(username=self.data['username'], password=self.data['password'])
        url = reverse('userprofiles_profile_change')
        response = self.client.get(url)
        self.assertFalse('first_name' in response.content and
                         'last_name' in response.content)
