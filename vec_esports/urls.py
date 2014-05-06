# The application-specific django urls file.
# ../proj-django/urls.py is the "main" urls file, and it links to here.

from django.conf.urls.defaults import *
from vec_esports.views import *

urlpatterns = patterns('',
    (r'^p_team/$', main_register),
    (r'^$', main_index),
    (r'^p_bracket/$', main_brackets),
    (r'^p_result/$', main_results),
    (r'^p_contact/$', main_contact),
)
