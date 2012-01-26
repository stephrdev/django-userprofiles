# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from userprofiles import settings as up_settings


def generate_token():
    return str(uuid.uuid4())

def generate_confirm_expire_date():
    return datetime.now() + timedelta(days=up_settings.EMAIL_VERIFICATION_DAYS)


class EmailVerification(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), blank=False)
    old_email = models.EmailField(_('Old e-mail address'))
    new_email = models.EmailField(_('New e-mail address'))

    token = models.CharField(_('Token'), max_length=40, default=generate_token)
    code = models.CharField(_('Code'), max_length=40, default=generate_token)

    is_approved = models.BooleanField(_('Approved'), default=False)
    is_expired = models.BooleanField(_('Expired'), default=False)

    expiration_date = models.DateTimeField(_('Expiration date'),
        default=generate_confirm_expire_date)

    def __unicode__(self):
        return '%s - %s/%s' % (self.user, self.old_email, self.new_email)

    def save(self, *args, **kwargs):
        if self.is_approved:
            EmailVerification.objects.filter(
                user=self.user, is_approved=False).update(is_expired=True)

            self.is_expired = True

            if self.user.email == self.old_email:
                self.user.email = self.new_email
                self.user.save()
        return super(EmailVerification, self).save(*args, **kwargs)

    class Meta:
        app_label = 'userprofiles'
        verbose_name = _('E-mail verification')
        verbose_name_plural = _('E-mail verifications')
