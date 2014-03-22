# The application-specific django urls file.
# ../proj-django/urls.py is the "main" urls file, and it links to here.

from django.conf.urls.defaults import *
from vec_esports.views import *

urlpatterns = patterns('',
    (r'^reg/$', team_register),
    (r'^bracket/$', bracket_make),
    (r'^$', main_esports),
    (r'^brackets.html$', brackets),
)
