from django.conf.urls import patterns, include, url

import views 
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BBS_Pro.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    (r'^reboot/$', views.reboot),
    (r'^fs_restart/$', views.fs_restart),
    (r'^fs_start/$', views.fs_start),
    (r'^fs_stop/$', views.fs_stop),

    (r'^imgur/$', views.upload),    

    (r'^$',views.index ),
    (r'^detail/(\d+)/$', views.bbs_detail),
    (r'^sub_comment/$', views.sub_comment),
    (r'^bbs_pub/$', views.bbs_pub),
    (r'^bbs_sub/$', views.bbs_sub),
    (r'^category/(\d+)/$',views.category),

    (r'^room/(\d+)/$', views.room),
    (r'^savemsg/$', views.savemsg),
    (r'^getmsg/$', views.getmsg),

    # (r'^pager/(?p<page>\d*)/$', views.pager),
    (r'^pager/(?P<page>\d*)/$', views.pager),

    )
