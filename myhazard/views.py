from django.shortcuts import render_to_response
from django.http import HttpResponse
from simplejson import dumps



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
               "features" : [
                    {"type": "Feature",
                     "geometry" : { "type" : "Point", "coordinates" :  [-8051914,2104311]}, 
                     "properties": {"name": "PDF One" }},
                    {"type": "Feature",
                     "geometry" : { "type" : "Point", "coordinates" :  [-8041914,2104311]}, 
                     "properties": {"name": "PDF Two" }},
                    {"type": "Feature",
                     "geometry" : { "type" : "Point", "coordinates" :  [-8031914,2104311]}, 
                     "properties": {"name": "PDF Three" }}
                    ]
               }),mimetype="application/json")
