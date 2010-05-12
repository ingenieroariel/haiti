from django.core.management.base import BaseCommand
from osgeo import gdal 
from osgeo import ogr
import urllib2

class Command(BaseCommand):
    help = 'Update the GeoNode application with data from GeoServer'
    args = '[none]'

    def handle(self, *args, **keywordargs):
        url = "http://unosat.web.cern.ch/unosat/rss/freemaps.asp?n=30"
        content = None
        try:
            handle = urllib2.urlopen(url)
            content = handle.read()
        except urllib2.HTTPError, e:
            print 'HTTP service for %s is down (HTTP Error: %d)' % (url, e.code)
        except:
            print 'HTTP service for %s is down.' %(url)
        _file = open("damagemaps.rss","w") 
        _file.write(content)
        
