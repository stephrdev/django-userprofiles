# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class Settings(object):
    def __init__(self, **kwargs):
        self.defaults = kwargs

    def __getattr__(self, key):
        return getattr(settings, 'USERPROFILES_%s' % key, self.defaults[key])


up_settings = Settings(
    REGISTRATION_FORM='userprofiles.forms.RegistrationForm',
    DOUBLE_CHECK_EMAIL=False,
    CHECK_UNIQUE_EMAIL=False,
    DOUBLE_CHECK_PASSWORD=False,
    REGISTRATION_FULLNAME=False,
    # Allows user to more easily control where registrations land
    REGISTRATION_REDIRECT='userprofiles_registration_complete',

    # Only use Email field on the form
    EMAIL_ONLY=False,

    # Automatically log in the user upon registration
    AUTO_LOGIN=False,

    USE_ACCOUNT_VERIFICATION=False,
    ACCOUNT_VERIFICATION_DAYS=7,

    EMAIL_VERIFICATION_DAYS=2,
    EMAIL_VERIFICATION_DONE_URL='userprofiles_email_change',

    USE_PROFILE=False,
    PROFILE_FORM='userprofiles.contrib.profiles.forms.ProfileForm',
    INLINE_PROFILE_ADMIN=False,

    PROFILE_ALLOW_EMAIL_CHANGE=False,
    PROFILE_CHANGE_DONE_URL='userprofiles_profile_change',
)


def validate_settings():
    if (up_settings.USE_ACCOUNT_VERIFICATION and
            'userprofiles.contrib.accountverification' not in settings.INSTALLED_APPS):
        raise ImproperlyConfigured('You need to add `userprofiles.contrib.accountverification` '
            'to INSTALLED_APPS to use account verification.')

    # These settings together make no sense
    if up_settings.USE_ACCOUNT_VERIFICATION and up_settings.AUTO_LOGIN:
        raise ImproperlyConfigured("You cannot use autologin with account verification")

    if up_settings.USE_PROFILE and 'userprofiles.contrib.profiles' not in settings.INSTALLED_APPS:
        raise ImproperlyConfigured('You need to add `userprofiles.contrib.profiles` '
            'to INSTALLED_APPS to use profiles.')

    if up_settings.PROFILE_ALLOW_EMAIL_CHANGE and up_settings.CHECK_UNIQUE_EMAIL:
        raise ImproperlyConfigured(
            'USERPROFILES_PROFILE_ALLOW_EMAIL_CHANGE cannot be activated '
            'when USERPROFILES_CHECK_UNIQUE_EMAIL is active.')

    if (up_settings.PROFILE_ALLOW_EMAIL_CHANGE
            and 'userprofiles.contrib.emailverification' in settings.INSTALLED_APPS):
        raise ImproperlyConfigured(
            'USERPROFILES_PROFILE_ALLOW_EMAIL_CHANGE cannot be activated '
            'when `userprofiles.contrib.emailverification` is used.')

validate_settings()
