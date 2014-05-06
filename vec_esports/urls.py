# The application-specific django urls file.
# ../proj-django/urls.py is the "main" urls file, and it links to here.

from django.conf.urls.defaults import *
from vec_esports.views import *

urlpatterns = patterns('',
    (r'^m_team/$', team_register),
    (r'^$', main_esports),
    (r'^m_bracket/$', brackets),
    (r'^m_result/$', results),
    (r'^m_admincontact/$', admin_contact),
)
