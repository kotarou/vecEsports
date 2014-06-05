# The application-specific django urls file.
# ../proj-django/urls.py is the "main" urls file, and it links to here.

from django.conf.urls.defaults import *
from vec_esports.views import *

urlpatterns = patterns('',
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^c_teams/$', 	main_teams,		{'change':True}),
    (r'^c_brackets/$', 	main_brackets,	{'change':True}),
    (r'^c_results/$', 	main_results,	{'change':True}),
    (r'^$', 			main_index),
    (r'^p_index/', 		main_index),
    (r'^p_contact/$', 	main_contact),  
    (r'^view/(?P<view>[a-z]+)/(?P<value>[a-zA-Z0-9!-~ ]+)/$',	main_views),
    (r'^viewall/(?P<view>[a-z]+)/$',					main_views,	{'single':False}),
    (r'^viewall/(?P<view>[a-z]+)/(?P<value>[a-z]+)/$',	main_views,	{'single':False}),
    (r'^secretadminlink/$', 	admin),  
)
