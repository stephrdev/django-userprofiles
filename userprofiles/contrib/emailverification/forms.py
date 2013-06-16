# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from userprofiles.contrib.emailverification.models import EmailVerification


class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField(label=_('New e-mail address'), required=True)

    def clean_new_email(self):
        new_email = self.cleaned_data['new_email']

        user_emails = User.objects.filter(email__iexact=new_email).count()
        verification_emails = EmailVerification.objects.filter(
            new_email__iexact=new_email, is_expired=False).count()
        if user_emails + verification_emails > 0:
            raise forms.ValidationError(_(
                'This email address is already in use. Please supply a different email address.'))

        return new_email

    def save(self, user):
        return EmailVerification.objects.create_new_verification(
            user, self.cleaned_data['new_email'])
