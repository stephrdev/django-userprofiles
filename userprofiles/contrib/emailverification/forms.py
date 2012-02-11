# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string
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

    def save(self, user=None):
        if not user:
            return None

        verification = EmailVerification.objects.create(user=user,
            old_email=user.email, new_email=self.cleaned_data['new_email'])

        context = {
            'user': user,
            'verification': verification,
            'site': Site.objects.get_current(),
        }

        subject = ''.join(render_to_string(
            'userprofiles/mails/emailverification_subject.html', context).splitlines())
        body = render_to_string('userprofiles/mails/emailverification.html', context)

        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
            [self.cleaned_data['new_email'],])

        return verification
