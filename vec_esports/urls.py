# The application-specific django urls file.
# ../proj-django/urls.py is the "main" urls file, and it links to here.

from django.conf.urls.defaults import *
from vec_esports.views import testbook, sign_post, main_esports

urlpatterns = patterns('',
    (r'^sign/$', sign_post),
    (r'^$', main_esports),
    (r'^test/$', testbook),
)
