from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from userprofiles import settings as up_settings

if up_settings.USERPROFILES_USE_ACCOUNT_VERIFICATION:
    from userprofiles.models import AccountVerification

class RegistrationForm(forms.Form):
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$',
        error_messages = {'invalid': _('This value may contain only letters, numbers and @/./+/-/_ characters.')})

    email = forms.EmailField(label=_('E-Mail'))
    email_repeat = forms.EmailField(label=_('E-Mail (again)'), required=True)

    password = forms.CharField(label=_('Password'),
        widget=forms.PasswordInput(render_value=False))
    password_repeat = forms.CharField(label=_('Password (again)'),
        widget=forms.PasswordInput(render_value=False))

    first_name = forms.CharField(label=_('First name'), required=False)
    last_name = forms.CharField(label=_('Last name'), required=False)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        if not up_settings.USERPROFILES_DOUBLE_CHECK_EMAIL:
            del self.fields['email_repeat']

        if not up_settings.USERPROFILES_DOUBLE_CHECK_PASSWORD:
            del self.fields['password_repeat']

        if not up_settings.USERPROFILES_REGISTRATION_FULLNAME:
            del self.fields['first_name']
            del self.fields['last_name']

    def clean_username(self):
        if User.objects.filter(username__iexact=self.cleaned_data['username']):
            raise forms.ValidationError(
                _(u'A user with that username already exists.'))

        return self.cleaned_data['username']

    def clean_email(self):
        if not up_settings.USERPROFILES_CHECK_UNIQUE_EMAIL:
            return self.cleaned_data['email']

        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(
                _(u'This email address is already in use. Please supply a different email address.'))

        return self.cleaned_data['email']

    def clean(self):
        if up_settings.USERPROFILES_DOUBLE_CHECK_EMAIL:
            if 'email' in self.cleaned_data and 'email_repeat' in self.cleaned_data:
                if self.cleaned_data['email'] != self.cleaned_data['email_repeat']:
                    raise forms.ValidationError(_('The two email addresses do not match.'))

        if up_settings.USERPROFILES_DOUBLE_CHECK_PASSWORD:
            if 'password' in self.cleaned_data and 'password_repeat' in self.cleaned_data:
                if self.cleaned_data['password'] != self.cleaned_data['password_repeat']:
                    raise forms.ValidationError(_('You must type the same password each time.'))

        return self.cleaned_data

    def save(self, *args, **kwargs):
        if up_settings.USERPROFILES_USE_ACCOUNT_VERIFICATION:
            new_user = AccountVerification.objects.create_inactive_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'],
                email=self.cleaned_data['email'],
            )
        else:
            new_user = User.objects.create(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'],
                email=self.cleaned_data['email']
            )

        if up_settings.USERPROFILES_REGISTRATION_FULLNAME:
            new_user.first_name = self.cleaned_data['first_name']
            new_user.last_name = self.cleaned_data['last_name']

            new_user.save()

        if hasattr(self, 'save_profile'):
            self.save_profile(new_user, *args, **kwargs)

        return new_user

