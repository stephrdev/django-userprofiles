# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('userprofiles.contrib.emailverification.views',
    url(r'^$', 'email_change', name='userprofiles_email_change'),
    url(r'^requested/$', 'email_change_requested',
        name='userprofiles_email_change_requested'),
    url(r'^verify/(?P<token>[0-9A-Za-z-]+)/(?P<code>[0-9A-Za-z-]+)/$',
        'email_change_approve', name='userprofiles_email_change_approve'),
)
