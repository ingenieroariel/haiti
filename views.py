from django.shortcuts import render_to_response

def haiti_index(request): 
    return render_to_response("haiti-index.html")

def data_search(request):
    if request.method == 'GET':
        try: 
            query = request.GET["query"]
        except: 
            query = "Hazard"
    if request.method == 'POST':
        query = request.POST["query"]
    return render_to_response("data_search.html",{"query": query})
