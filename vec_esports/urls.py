# The application-specific django urls file.
# ../proj-django/urls.py is the "main" urls file, and it links to here.

from django.conf.urls.defaults import *
from vec_esports.views import *

urlpatterns = patterns('',
    (r'^p_teams/$', main_register),
    (r'^$', main_index),
    (r'^p_index/', main_index),
    (r'^p_brackets/$', main_brackets),
    (r'^p_results/$', main_results),
    (r'^p_contact/$', main_contact),
    (r'^v_teams/$', view_teams),
    (r'^v_brackets/$', view_brackets),
    (r'^v_results/$', view_results),
)
