# -*- coding: utf-8 -*-
import uuid

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from userprofiles.settings import up_settings


class RegistrationForm(forms.Form):
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.-]+$', error_messages={'invalid': _(
            'This value may contain only letters, numbers and ./-/_ characters.')})

    email = forms.EmailField(label=_('E-mail'))
    email_repeat = forms.EmailField(label=_('E-mail (repeat)'), required=True)

    password = forms.CharField(label=_('Password'),
        widget=forms.PasswordInput(render_value=False))
    password_repeat = forms.CharField(label=_('Password (repeat)'),
        widget=forms.PasswordInput(render_value=False))

    first_name = forms.CharField(label=_('First name'), required=False)
    last_name = forms.CharField(label=_('Last name'), required=False)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        if not up_settings.DOUBLE_CHECK_EMAIL:
            del self.fields['email_repeat']

        if not up_settings.DOUBLE_CHECK_PASSWORD:
            del self.fields['password_repeat']

        if not up_settings.REGISTRATION_FULLNAME:
            del self.fields['first_name']
            del self.fields['last_name']

        if up_settings.EMAIL_ONLY:
            self.fields['username'].widget = forms.widgets.HiddenInput()
            self.fields['username'].required = False

    def _generate_username(self):
        """ Generate a unique username """
        while True:
            # Generate a UUID username, removing dashes and the last 2 chars
            # to make it fit into the 30 char User.username field. Gracefully
            # handle any unlikely, but possible duplicate usernames.
            username = str(uuid.uuid4())
            username = username.replace('-', '')
            username = username[:-2]

            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                return username

    def clean_username(self):
        if up_settings.EMAIL_ONLY:
            username = self._generate_username()
        else:
            username = self.cleaned_data['username']
            if User.objects.filter(username__iexact=username):
                raise forms.ValidationError(
                    _(u'A user with that username already exists.'))

        return username

    def clean_email(self):
        if not up_settings.CHECK_UNIQUE_EMAIL:
            return self.cleaned_data['email']

        new_email = self.cleaned_data['email']

        emails = User.objects.filter(email__iexact=new_email).count()

        if up_settings.USE_EMAIL_VERIFICATION:
            from userprofiles.contrib.emailverification.models import EmailVerification

            emails += EmailVerification.objects.filter(
                new_email__iexact=new_email, is_expired=False).count()

        if emails > 0:
            raise forms.ValidationError(
                _(u'This email address is already in use. Please supply a different email address.'))

        return new_email

    def clean(self):
        if up_settings.DOUBLE_CHECK_EMAIL:
            if 'email' in self.cleaned_data and 'email_repeat' in self.cleaned_data:
                if self.cleaned_data['email'] != self.cleaned_data['email_repeat']:
                    raise forms.ValidationError(_('The two email addresses do not match.'))

        if up_settings.DOUBLE_CHECK_PASSWORD:
            if 'password' in self.cleaned_data and 'password_repeat' in self.cleaned_data:
                if self.cleaned_data['password'] != self.cleaned_data['password_repeat']:
                    raise forms.ValidationError(_('You must type the same password each time.'))

        return self.cleaned_data

    def save(self, *args, **kwargs):
        if up_settings.USE_ACCOUNT_VERIFICATION:
            from userprofiles.contrib.accountverification.models import AccountVerification

            new_user = AccountVerification.objects.create_inactive_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'],
                email=self.cleaned_data['email'],
            )
        else:
            new_user = User.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'],
                email=self.cleaned_data['email']
            )

        if up_settings.REGISTRATION_FULLNAME:
            new_user.first_name = self.cleaned_data['first_name']
            new_user.last_name = self.cleaned_data['last_name']

            new_user.save()

        if hasattr(self, 'save_profile'):
            self.save_profile(new_user, *args, **kwargs)

        return new_user
