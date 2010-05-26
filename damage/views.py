# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request): 
    return render_to_response("damage.html")

def atlas(request): 
    return render_to_response("damage-atlas.html")

def reports(request): 
    return render_to_response("damage-reports.html")

def new_report(rquest):
    return render_to_response("damage-reports-new.html")
