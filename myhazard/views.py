from django.shortcuts import render_to_response

def index(request): 
    return render_to_response("hazard.html")

def maps(request):
    return render_to_response("hazard-maps.html")

def reports(request): 
    return render_to_response("hazard-reports.html")

def data(request): 
    return render_to_response("data.html")
