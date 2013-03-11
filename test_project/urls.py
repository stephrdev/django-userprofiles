from django.conf.urls import patterns, include


urlpatterns = patterns('',
    (r'^userprofiles/', include('userprofiles.urls')),
)
