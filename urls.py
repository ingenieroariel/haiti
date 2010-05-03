from django.conf.urls.defaults import *
import geonode
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^hazard/$',include('haiti.myhazard.urls')),
    (r'^damage/$',include('haiti.damage.urls')),
    (r'^geonode/$', include('geonode.urls')),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': "static"}),


)
