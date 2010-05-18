from django.core.management.base import BaseCommand
import urllib2
from elementtree import ElementTree
from haiti.damage.models import DamageMap
from django.contrib.gis.geos import Point

class Damage:
    def __init__(self,title,country,category,guid,GLIDE,pubDate,description,point,polygon):
        self.title = title.text
        self.country = country.text
        self.category = category.text
        self.guid = guid.text
        self.GLIDE = GLIDE.text
        self.pubDate = pubDate.text
        self.description = description.text
        try:
            self.point = point.text
            self.polygon = polygon.text
        except:
            self.point = None
            self.polygon = None

def process_geom(point): 
    coords = point.split(" ")
    point = Point(float(coords[1]),float(coords[0]))
    return point
                   
class Command(BaseCommand):
    help = 'Update the GeoNode application with data from GeoServer'
    args = '[none]'

    def handle(self, *args, **keywordargs):
        url = "http://unosat.web.cern.ch/unosat/rss/freemaps.asp?n=500"
        content = None
        try:
            handle = urllib2.urlopen(url)
            content = handle.read()
        except urllib2.HTTPError, e:
            print 'HTTP service for %s is down (HTTP Error: %d)' % (url, e.code)
        except:
            print 'HTTP service for %s is down.' %(url)        
        tree = ElementTree.fromstring(content)
        items = tree.getiterator("item")
        collection = []
        for item in items: 
            damage = Damage(item.find("title"),item.find("country"),
                            item.find("category"),item.find("guid"),
                            item.find("GLIDE"),item.find("pubDate"),
                            item.find("description"),
                            item.find("{http://www.georss.org/georss}point"),
                            item.find("{http://www.georss.org/georss}polygon"))
            if damage.country == "Haiti":
                collection.append(damage)
        for damage in collection:
            if damage.point != None:
                DamageMap(title=damage.title,country=damage.country,
                          category=damage.category,guid=damage.guid,
                          glide=damage.GLIDE,pubdate=damage.pubDate,
                          description=damage.description,
                          point=process_geom(damage.point).wkt
                          ).save()
