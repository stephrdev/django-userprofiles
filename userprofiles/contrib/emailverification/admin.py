# -*- coding: utf-8 -*-
from django.contrib import admin

from userprofiles.contrib.emailverification.models import EmailVerification


class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'old_email', 'new_email', 'expiration_date',
        'is_approved', 'is_expired')
    list_filter = ('is_approved', 'is_expired')

admin.site.register(EmailVerification, EmailVerificationAdmin)
