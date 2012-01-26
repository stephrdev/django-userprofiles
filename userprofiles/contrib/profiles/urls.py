from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('userprofiles.contrib.profiles.views',
    url(r'^$', 'profile',
        name='userprofiles_profile'),
    url(r'^change/$', 'profile_change',
        name='userprofiles_profile_change'),
)
