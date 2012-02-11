# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


REGISTRATION_FORM = getattr(
    settings, 'USERPROFILES_REGISTRATION_FORM',
    'userprofiles.forms.RegistrationForm')

INLINE_PROFILE_ADMIN = getattr(
    settings, 'USERPROFILES_INLINE_PROFILE_ADMIN', False)

DOUBLE_CHECK_EMAIL = getattr(
    settings, 'USERPROFILES_DOUBLE_CHECK_EMAIL', False)

CHECK_UNIQUE_EMAIL = getattr(
    settings, 'USERPROFILES_CHECK_UNIQUE_EMAIL', False)

DOUBLE_CHECK_PASSWORD = getattr(
    settings, 'USERPROFILES_DOUBLE_CHECK_PASSWORD', False)

REGISTRATION_FULLNAME = getattr(
    settings, 'USERPROFILES_REGISTRATION_FULLNAME', False)


USE_ACCOUNT_VERIFICATION = getattr(
    settings, 'USERPROFILES_USE_ACCOUNT_VERIFICATION', False)

if (USE_ACCOUNT_VERIFICATION and
    'userprofiles.contrib.accountverification' not in settings.INSTALLED_APPS):
    raise ImproperlyConfigured('You need to add `userprofiles.contrib.accountverification` '
        'to INSTALLED_APPS to use account verification.')

ACCOUNT_VERIFICATION_DAYS = getattr(
    settings, 'USERPROFILES_ACCOUNT_VERIFICATION_DAYS', 7)


EMAIL_VERIFICATION_DAYS = getattr(
    settings, 'USERPROFILES_EMAIL_VERIFICATION_DAYS', 2)

EMAIL_VERIFICATION_DONE_URL = getattr(
    settings, 'USERPROFILES_EMAIL_VERIFICATION_DONE_URL',
    'userprofiles_email_change')


USE_PROFILE = getattr(
    settings, 'USERPROFILES_USE_PROFILE', False)

if not USE_PROFILE and 'userprofiles.contrib.profiles' in settings.INSTALLED_APPS:
    raise ImproperlyConfigured('You need to activate profiles to use '
        '`userprofiles.contrib.accountverification`')

PROFILE_FORM = getattr(
    settings, 'USERPROFILES_PROFILE_FORM',
    'userprofiles.contrib.profiles.forms.ProfileForm')

PROFILE_ALLOW_EMAIL_CHANGE = getattr(
    settings, 'USERPROFILES_PROFILE_ALLOW_EMAIL_CHANGE', False)

if PROFILE_ALLOW_EMAIL_CHANGE and CHECK_UNIQUE_EMAIL:
    raise ImproperlyConfigured(
        'USERPROFILES_PROFILE_ALLOW_EMAIL_CHANGE cannot be activated '
        'when USERPROFILES_CHECK_UNIQUE_EMAIL is active.')

if (PROFILE_ALLOW_EMAIL_CHANGE
    and 'userprofiles.contrib.emailverification' in settings.INSTALLED_APPS):
    raise ImproperlyConfigured(
        'USERPROFILES_PROFILE_ALLOW_EMAIL_CHANGE cannot be activated '
        'when `userprofiles.contrib.emailverification` is used.')

PROFILE_CHANGE_DONE_URL = getattr(
    settings, 'USERPROFILES_PROFILE_CHANGE_DONE_URL',
    'userprofiles_profile_change')
