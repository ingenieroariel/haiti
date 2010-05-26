# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from haiti.damage.models import DamageReports, HaitiAdmin, DamageCensus
import simplejson as json
from django.contrib.gis.geos import GEOSGeometry

def make_geojson(collection): 
    pass 

def make_json(col):
    return [{
            "gid" : x.gid,
            "pid" : x.pid, 
            "grade" : x.grade,
            "confidence": x.confidence,
            "comment": x.comment} for x in col]

def make_group(col):
    grade_one = 0 
    grade_two = 0 
    grade_three = 0 
    grade_four = 0 
    grade_five = 0 
    for record in col: 
        if record.grade == "1":
            grade_one = grade_one + 1 
        if record.grade == "2": 
            grade_two = grade_two + 1 
        if record.grade == "3":
            grade_three = grade_three + 1 
        if record.grade == "4": 
            grade_four = grade_four + 1 
        if record.grade == "5": 
            grade_five = grade_five + 1 
    return {"one":grade_one, 
            "two" : grade_two, 
            "three" : grade_three,
            "four" : grade_four,
            "five" : grade_five} 

def index(request): 
    return render_to_response("damage.html")

def atlas(request): 
    return render_to_response("damage-atlas.html")

def reports(request): 
    reports = DamageReports.objects.all()
    return render_to_response("damage-reports.html",
                              {
            "reports" :reports,
            })

def get_damage_census(request): 
    if request.method == "POST": 
        geom = request.POST.get("geom")
        search = GEOSGeometry(geom)
        census = DamageCensus.objects.filter(the_geom__within=search)        
    else: 
        return HttpResponse("Not allowed")
    return HttpResponse(json.dumps(make_group(census)),mimetype="application/json")

def new_report(rquest):
    departments = HaitiAdmin.objects.all()
    return render_to_response("damage-reports-new.html", 
                              {"departments" : departments})
