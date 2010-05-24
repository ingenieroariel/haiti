import json 
from django.conf import settings

def radius_for(scale): 
    """
    Given a scale denominator for the viewport, produce the proper buffer radius
    for the report process. 
    """
    return 0.012

def extract_params(request):
    """
    Examine a report request and extract the parameters that should be 
    included in the corresponding WPS request.
    """
    if request.method == "POST":
        try:
            params = json.loads(request.raw_post_data)
            params["radius"] = radius_for(params["scale"])
            del params["scale"]
            return params
        except:
            pass
    elif request.method == 'GET': 
        try:
            params = json.loads(request.GET['q'])
            params["radius"] = radius_for(params["scale"])
            del params["scale"]
            return params
        except:
            pass
    return {}

def request_rest_process(process, params): 
    """
    Make a REST request for the WPS process named, with the provided parameters.
    """
    url = "%srest/process/%s" % (settings.GEOSERVER_BASE_URL, process)
    user, pw = settings.GEOSERVER_CREDENTIALS
    http = Http()
    http.add_credentials(user, pw)
    response, content = http.request(url, "POST", json.dumps(params))
    if (response.status is not 200):
        raise Exception("REST process responded with\nStatus: {0}\nResponse:\n{1}".format(response.status, content))
    return json.loads(content)


def report(request, format): 
    params = extract_params(request)
    result = request_rest_process("hazard", params)
    if format == 'html':
        data_for_report = {'political': result.get('political', None)}
        
        geometry = params.get("geometry")
        if geometry.get("type") == "Point":
            geom_data = (geometry.get("coordinates")[0], geometry.get("coordinates")[1]) 
        elif geometry.get("type") == "Line" or geometry.get("type") == "LineString":
            geom_data = "[Distance]"
        elif geometry.get("type") == "Polygon":
            geom_data = "[Area]"

        statistics = dict()
        for layer, stats in result['statistics'].items():
            layer_record = Layer.objects.get(typename=layer)
            period = Period.objects.get(layer=layer_record)
            hazard = period.hazard.name
            if data_for_report.get(hazard):            
                statistics[hazard].append((period.length,stats))
                statistics[hazard].sort() #ensure nice ordering
            else:
                statistics[hazard] = [(period.length,stats)]
                md = layer_record.metadata()
                if md: 
                    stats['author'] = getattr(md,'title',None)
                if md:
                    stats['url'] = getattr(md, 'url', None)
        data_for_report['statistics'] = statistics
        return render_to_response("hazard/report.html", RequestContext(request, {
            "data": data_for_report,
            "geom_data": geom_data
        }))
    elif format == 'pdf':
        return render_pdf_response(result)
    else:
        raise Exception("Report requested in invalid format. (Expects .html or .pdf)")
