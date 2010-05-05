from django.conf.urls.defaults import *
import geonode 
from haiti import views

urlpatterns = patterns('',
    url(r'^$',views.haiti_index,name="site-index"),
    url(r'^data/search/$',views.data_search,name="data-search"),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
     {'document_root': "static"}),
)

urlpatterns += patterns('',
    (r'^geonode/', include('geonode.urls')),
)


urlpatterns += patterns('haiti.myhazard.views',
    url(r'^hazard/$','index',name='hazard-index'),
    url(r'^hazard/maps/$','maps',name='hazard-maps'),
    url(r'^hazard/reports/$','reports',name='hazard-reports'),
)

urlpatterns += patterns('haiti.damage.views',
    url(r'^damage/$','index',name='damage-index'),
)
