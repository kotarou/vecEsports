# The application-specific django urls file.
# ../proj-django/urls.py is the "main" urls file, and it links to here.

from django.conf.urls.defaults import *
from vec_esports.views import *

urlpatterns = patterns('',
    (r'^c_teams/$', 	main_teams,		{'change':True}),
    (r'^v_teams/$', 	main_teams,		{'change':False}),
    (r'^c_brackets/$', 	main_brackets,	{'change':True}),
    (r'^v_brackets/$', 	main_brackets,	{'change':False}),
    (r'^c_results/$', 	main_results,	{'change':True}),
    (r'^v_results/$', 	main_results,	{'change':False}),
    (r'^$', 			main_index),
    (r'^p_index/', 		main_index),
    (r'^p_contact/$', 	main_contact),  
)
