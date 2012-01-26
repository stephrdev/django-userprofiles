# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include

from django.conf import settings


urlpatterns = patterns('userprofiles.views',
    url(r'^register/$', 'registration', name='userprofiles_registration'),
    url(r'^register/complete/$', 'registration_complete',
        name='userprofiles_registration_complete'),
)

if 'userprofiles.contrib.accountverification' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        (r'^activate/', include('userprofiles.contrib.accountverification.urls')),
    )

if 'userprofiles.contrib.emailverification' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        (r'^email/', include('userprofiles.contrib.emailverification.urls')),
    )

if 'userprofiles.contrib.profiles' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        (r'^profile/', include('userprofiles.contrib.profiles.urls')),
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
