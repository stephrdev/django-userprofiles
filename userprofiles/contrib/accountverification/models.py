# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import random
import re
import uuid

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.hashcompat import sha_constructor
from django.utils.translation import gettext_lazy as _

from userprofiles import settings as up_settings

SHA1_RE = re.compile('^[a-f0-9]{40}$')


class AccountVerificationManager(models.Manager):
    def activate_user(self, activation_key):
        if SHA1_RE.search(activation_key):
            try:
                verification = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False

            if not verification.activation_key_expired():
                user = verification.user
                user.is_active = True
                user.save()

                verification.activation_key = self.model.ACTIVATED
                verification.save()

                return user

        return False

    def create_inactive_user(self, username, password, email):
        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = False
        new_user.save()

        account_verification = self.create_verification(new_user)
        current_site = Site.objects.get_current()

        subject = ''.join(render_to_string(
            'userprofiles/mails/activation_email_subject.html',
            {'site': current_site}).splitlines())

        message = render_to_string('userprofiles/mails/activation_email.html', {
            'activation_key': account_verification.activation_key,
            'expiration_days': up_settings.ACCOUNT_VERIFICATION_DAYS,
            'site': current_site})

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [new_user.email])

        return new_user

    def create_verification(self, user):
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        activation_key = sha_constructor(salt + str(uuid.uuid4())).hexdigest()
        return self.create(user=user, activation_key=activation_key)

    def delete_expired_users(self):
        for verification in self.all():
            if verification.activation_key_expired():
                user = verification.user
                if not user.is_active:
                    user.delete()

class AccountVerification(models.Model):
    ACTIVATED = 'ALREADY_ACTIVATED'

    user = models.ForeignKey(User, unique=True, verbose_name=_('User'))
    activation_key = models.CharField(_('Activation key'), max_length=40)

    objects = AccountVerificationManager()

    def __unicode__(self):
        return u'Account verification: %s' % self.user

    def activation_key_expired(self):
        expiration_date = timedelta(days=up_settings.ACCOUNT_VERIFICATION_DAYS)
        return (self.activation_key == self.ACTIVATED
            or (self.user.date_joined + expiration_date <= datetime.now()))
    activation_key_expired.boolean = True

    class Meta:
        app_label = 'userprofiles'
        verbose_name = _('Account verification')
        verbose_name_plural = _('Account verifications')
