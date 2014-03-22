from django.conf.urls.defaults import *
from vec_esports.views import main_page, sign_post

urlpatterns = patterns('',
    (r'^sign/$', sign_post),
    (r'^$', main_page),
)
