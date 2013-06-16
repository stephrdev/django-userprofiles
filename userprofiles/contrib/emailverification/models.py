# -*- coding: utf-8 -*-
from datetime import timedelta
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


from userprofiles.settings import up_settings


def generate_token():
    return str(uuid.uuid4())


def generate_confirm_expire_date():
    return timezone.now() + timedelta(days=up_settings.EMAIL_VERIFICATION_DAYS)


class EmailVerificationManager(models.Manager):

    def create_new_verification(self, user, new_email):
        """Creates a new verification and sends the respective e-mail."""

        verification = self.create(user=user, old_email=user.email,
                                   new_email=new_email)

        context = {
            'user': user,
            'verification': verification,
            'site': Site.objects.get_current(),
        }

        subject = ''.join(render_to_string(
            'userprofiles/mails/emailverification_subject.html', context).splitlines())
        body = render_to_string('userprofiles/mails/emailverification.html', context)

        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [new_email])

        return verification

    def get_pending(self, user):
        """Returns a queryset for all the still pending verifications of the
        given user. This should return either one or no element."""
        return self.get_query_set().filter(
            user=user, is_approved=False, is_expired=False)


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

    objects = EmailVerificationManager()

    def __unicode__(self):
        return '%s - %s/%s' % (self.user, self.old_email, self.new_email)

    def save(self, *args, **kwargs):
        EmailVerification.objects.exclude(pk=self.pk).filter(user=self.user,
            is_approved=False).update(is_expired=True)

        if self.is_approved:
            self.is_expired = True

            if self.user.email == self.old_email:
                self.user.email = self.new_email
                self.user.save()

        return super(EmailVerification, self).save(*args, **kwargs)

    class Meta:
        app_label = 'userprofiles'
        verbose_name = _('E-mail verification')
        verbose_name_plural = _('E-mail verifications')
