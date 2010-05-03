from django.conf.urls.defaults import *
from haiti.damage import views

urlpatterns = patterns('',
    # Example:
    (r'^/',views.index),
)
