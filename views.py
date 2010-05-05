from django.shortcuts import render_to_response

def index(request): 
    return render_to_response("index.html")

def data_search(request):
    return render_to_response("data_search.html")
