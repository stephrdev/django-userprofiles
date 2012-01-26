# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('userprofiles.contrib.accountverification.views',
    url(r'^(?P<activation_key>\w+)/$', 'registration_activate',
        name='userprofiles_registration_activate'),
)
