from django.shortcuts import render_to_response
from django.http import HttpResponse
from simplejson import dumps
from haiti.damage.models import DamageMap


def index(request): 
    return render_to_response("hazard.html")

def maps(request):
    return render_to_response("hazard-maps.html")

def reports(request): 
    return render_to_response("hazard-reports.html")

def data(request): 
    return render_to_response("data.html")


def maps_json(request):
    return HttpResponse(
        dumps({"type": "FeatureCollection",
               "features" : [ {"type": "Feature", 
                               "geometry": { "type": "Point", "coordinates": 
                                             [x.polygon.x, x.polygon.y]},
                              "properties" : {"name" : x.title,
                                              "description" : x.description}
                               }                              
                              for x in DamageMap.objects.all()]
               }),mimetype="application/json")
