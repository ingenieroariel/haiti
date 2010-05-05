from django.shortcuts import render_to_response

def haiti_index(request): 
    return render_to_response("haiti-index.html")

def data_search(request):
    return render_to_response("data_search.html")
