# The base django urls file.
# We want to have a url file per application.
# So this file links to each so called "subfile"

from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('vec_esports.urls')),
)

#urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Django_AppEngine..views.home', name='home'),
    # url(r'^Django_AppEngine./', include('Django_AppEngine..foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
#)
