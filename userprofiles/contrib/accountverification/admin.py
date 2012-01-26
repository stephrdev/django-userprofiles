# -*- coding: utf-8 -*-
from django.contrib import admin

from userprofiles.contrib.accountverification.models import AccountVerification


class AccountVerificationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'activation_key_expired')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

admin.site.register(AccountVerification, AccountVerificationAdmin)
