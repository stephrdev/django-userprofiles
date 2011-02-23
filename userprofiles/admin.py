from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from userprofiles import settings as up_settings

if up_settings.USERPROFILES_USE_PROFILE and up_settings.USERPROFILES_INLINE_PROFILE_ADMIN:
    from userprofiles.utils import UserProfile

    admin.site.unregister(User)

    class UserProfileInline(admin.StackedInline):
        model = UserProfile
        extra = 1
        max_num = 1

    class UserProfileAdmin(UserAdmin):
        inlines = [UserProfileInline,]

    admin.site.register(User, UserProfileAdmin)

if up_settings.USERPROFILES_USE_ACCOUNT_VERIFICATION:
    from userprofiles.models import AccountVerification

    class AccountVerificationAdmin(admin.ModelAdmin):
        list_display = ('__unicode__', 'activation_key_expired')
        search_fields = ('user__username', 'user__first_name',
                         'user__last_name')

    admin.site.register(AccountVerification, AccountVerificationAdmin)

