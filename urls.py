from django.conf.urls.defaults import *
import geonode 
from geonode.proxy.views import proxy
from haiti import views
from geonode.maps.views import metadata_search


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',views.haiti_index,name="site-index"),
    url(r'^data/browse/$',views.browse_data,name="data-search"),
    url(r'^data/search/$',metadata_search,name="ajax-search"),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
     {'document_root': "static"}),
)

urlpatterns += patterns('',
    (r'^geonode/', include('geonode.urls')),
    (r'^proxy/',proxy),
    (r'^admin/', include(admin.site.urls)),

)

urlpatterns += patterns('haiti.report.views',
    (r'^/report(.(?P<format>html|pdf))?', 'report'),
)


urlpatterns += patterns('haiti.myhazard.views',
    url(r'^hazard/$','index',name='hazard-index'),
    url(r'^hazard/maps/$','maps',name='hazard-maps'),
    url(r'^hazard/maps.json$','maps_json',name='hazard-maps-json'),
    url(r'^hazard/reports/$','reports',name='hazard-reports'),
)

urlpatterns += patterns('haiti.damage.views',
    url(r'^damage/$','index',name='damage-index'),
    url(r'^damage/reports$','reports',name='damage-reports'),

)
