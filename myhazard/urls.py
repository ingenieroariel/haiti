from django.conf.urls.defaults import *
from haiti.myhazard import views

urlpatterns = patterns('',
    # Example:
    (r'^',views.index),
)
