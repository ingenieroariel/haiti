# Create your views here.
#from django.http import HttpResponse
from django.shortcuts import render_to_response
from haiti.damage.models import DamageReports, HaitiAdmin

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

def new_report(rquest):
    departments = HaitiAdmin.objects.all()
    return render_to_response("damage-reports-new.html", 
                              {"departments" : departments})
