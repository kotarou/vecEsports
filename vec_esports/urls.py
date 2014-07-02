# The application-specific django urls file.
# ../proj-django/urls.py is the "main" urls file, and it links to here.

from django.conf.urls.defaults import *
from vec_esports.views import *

urlpatterns = patterns('',
    # Auth
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),

    # Admin links
    (r'^admin/matchups/$',      main_brackets,	{'change':True}),
    (r'^admin/results/$',       main_results,	{'change':True}),
    
    # Generic pages
    (r'^$',             main_index),
    (r'^contact/$',     main_contact), 

    # Registration
    (r'^register/$',    main_teams,     {'change':True, 're':False}),
    (r'^reregister/$',  main_teams,     {'change':True, 're':True}),

    # Links to view infomation based on URL
    (r'^view/(?P<view>[a-z]+)/(?P<value>[a-zA-Z0-9!-~ ]+)/$',   main_views),
    (r'^viewall/team/all/$',                            main_views,	{'view':'team', 'mode':'all'}),
    (r'^viewall/team/current/$',                        main_views,	{'view':'team', 'mode':'current'}),
    
    # Page where I tack manual database edits on
    (r'^secretadminlink/$', 	admin),  

    # Legacy links
    (r'^c_teams/$',     main_teams,     {'change':True, 're':False}),     
    (r'^p_index/',      main_index),
    (r'^p_contact/$',   main_contact),  
    # Legacy Admin
    (r'^c_brackets/$',  main_brackets,  {'change':True}),
    (r'^c_results/$',   main_results,   {'change':True}),
)
