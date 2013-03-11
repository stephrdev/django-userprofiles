from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from test_project.test_accounts.models import Profile


@override_settings(USERPROFILES_USE_PROFILE=True, AUTH_PROFILE_MODULE='test_accounts.Profile')
class ViewTests(TestCase):
    def setUp(self):
        self.data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'new_email': 'anotheremail@example.com',
            'password': 'newuserpass',
            'first_name': 'John',
            'last_name': 'Doe',
            'short_info': 'Short Info Test!'
        }
        self.user = User.objects.create_user(self.data['username'], self.data['email'],
            self.data['password'])
        Profile(user=self.user).save()

    def tearDown(self):
        User.objects.get(username=self.data['username']).delete()

    def test_profile_view(self):
        self.client.login(username=self.data['username'], password=self.data['password'])

        url = reverse('userprofiles_profile')
        response = self.client.get(url)

        self.assertEqual(response.context['user'], self.user)

    @override_settings(USERPROFILES_REGISTRATION_FULLNAME=True)
    def test_profile_change_fullname_enabled(self):
        self.client.login(username=self.data['username'], password=self.data['password'])

        change_url = reverse('userprofiles_profile_change')

        response = self.client.get(change_url)
        self.assertTrue('first_name' in response.context['form'].fields and
            'last_name' in response.context['form'].fields)

        self.client.post(change_url, {'first_name': self.data['first_name'],
            'last_name': self.data['last_name']})
        response = self.client.get(change_url)

        self.assertTrue(User.objects.filter(pk=self.user.pk,
            first_name=self.data['first_name'], last_name=self.data['last_name']).exists())

    def test_profile_change_fullname_disabled(self):
        self.client.login(username=self.data['username'], password=self.data['password'])

        change_url = reverse('userprofiles_profile_change')

        response = self.client.get(change_url)
        self.assertFalse('first_name' in response.context['form'].fields and
            'last_name' in response.context['form'].fields)

    @override_settings(USERPROFILES_PROFILE_ALLOW_EMAIL_CHANGE=True)
    def test_profile_change_email_enabled(self):
        self.client.login(username=self.data['username'], password=self.data['password'])

        change_url = reverse('userprofiles_profile_change')

        response = self.client.get(change_url)
        self.assertTrue('email' in response.context['form'].fields)

        self.client.post(change_url, {'email': self.data['new_email']})
        response = self.client.get(change_url)

        self.assertTrue(User.objects.filter(pk=self.user.pk,
            email=self.data['new_email']).exists())

#    def test_profile_change_test_extra_fields(self):
#        self.assertEqual(self.user.profile.short_info, '')
#
#        self.client.login(username=self.data['username'], password=self.data['password'])
#
#        change_url = reverse('userprofiles_profile_change')
#
#        response = self.client.get(change_url)
#
#        self.assertTrue('short_info' in response.context['form'].fields)
#
#        self.client.post(change_url, {'short_info': self.data['short_info']})
#        response = self.client.get(change_url)
#
#        self.assertEqual(self.user.profile.short_info, self.data['short_info'])
