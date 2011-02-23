from django.conf.urls.defaults import *

from userprofiles import settings as up_settings

urlpatterns = patterns('userprofiles.views',
    url(r'^register/$', 'registration', name='userprofiles_registration'),
    url(r'^register/complete/$', 'registration_complete',
        name='userprofiles_registration_complete'),
)

if up_settings.USERPROFILES_USE_ACCOUNT_VERIFICATION:
    urlpatterns += patterns('userprofiles.views',
        url(r'^activate/(?P<activation_key>\w+)/$', 'registration_activate',
            name='userprofiles_registration_activate'),
    )

if up_settings.USERPROFILES_USE_PROFILE and up_settings.USERPROFILES_USE_PROFILE_VIEW:
    urlpatterns += patterns('userprofiles.views',
        url(r'^profile/$', 'profile',
            name='userprofiles_profile'),
    )


urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'userprofiles/login.html'},
        name='auth_login'),
    url(r'^logout/$', 'logout', {'template_name': 'userprofiles/logged_out.html'},
        name='auth_logout'),
    url(r'^password/change/$', 'password_change',
        {'template_name': 'userprofiles/password_change.html'},
        name='auth_password_change'),
    url(r'^password/change/done/$', 'password_change_done',
        {'template_name': 'userprofiles/password_change_done.html'},
        name='auth_password_change_done'),
    url(r'^password/reset/$', 'password_reset',
        {'template_name': 'userprofiles/password_reset.html',
         'email_template_name': 'userprofiles/mails/password_reset_email.html'},
        name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'password_reset_confirm',
        {'template_name': 'userprofiles/password_reset_confirm.html'},
        name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$', 'password_reset_complete',
        {'template_name': 'userprofiles/password_reset_complete.html'},
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$', 'password_reset_done',
        {'template_name': 'userprofiles/password_reset_done.html'},
        name='auth_password_reset_done'),
)

