# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from haiti.damage.models import DamageReports, HaitiAdmin, DamageCensus
import simplejson as json
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings
from owslib.wms import WebMapService
import StringIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
import StringIO 
import datetime

def make_geojson(collection): 
    pass 

def make_json(col):
    return [{
            "gid" : x.gid,
            "pid" : x.pid, 
            "grade" : x.grade,
            "confidence": x.confidence,
            "comment": x.comment} for x in col]

def group_by_grade(col):
    counts =  [0,0,0,0,0]
    for record in col: 
        if record.grade == "1":
            counts[0] = counts[0] + 1  
        if record.grade == "2": 
            counts[1] = counts[1] + 1 
        if record.grade == "3":
            counts[2] = counts[2] + 1 
        if record.grade == "4": 
            counts[3] = counts[3] + 1 
        if record.grade == "5": 
            counts[4] = counts[4] + 1 
    return counts 

def build_wms_image(bbox):
    url = "%s/wms" % settings.GEOSERVER_BASE_URL
    wms = WebMapService(url, version='1.1.1')
    img = wms.getmap(layers=['haiti'],
                     srs='EPSG:4326',
                     bbox=bbox,
                     size=(1000, 1000),
                     bgcolor="#b5d0d0",
                     format='image/jpeg',
                     transparent=True)
    return img

def get_map(map): 
    img_buffer = StringIO.StringIO(map.read())
    return Image(img_buffer,5*inch, 3*inch)
    
def make_pdf_response(largeMap): 
    response = HttpResponse(mimetype="application/pdf")
    response["Content-Disposition"] = "attachment; filename=report.pdf"
    styles = getSampleStyleSheet()    
    doc = SimpleDocTemplate(response)
    Title = Paragraph("Damage Assessment Report",styles["Title"])
    Story = [Spacer(1,2*inch)]
    Story.append(Title)
    Story.append(get_map(largeMap))
    doc.build(Story)
    return response

def index(request): 
    return render_to_response("damage.html")

def atlas(request): 
    return render_to_response("damage-atlas.html")

def reports(request): 
    reports = DamageReports.objects.all()
    return render_to_response("damage-reports.html",{"reports" :reports})

def create_report(request):
    report_stats = list(request.session["report_table"])
    report_bbox = request.session["report_bbox"]
    largeMap = build_wms_image(report_bbox)
    return make_pdf_response(largeMap)

def get_damage_census(request): 
    if request.method == "POST": 
        geom = request.POST.get("geom")
        search = GEOSGeometry(geom)
        census = DamageCensus.objects.filter(the_geom__within=search)        
        grouped = group_by_grade(census)
        request.session["report_bbox"] = search.extent        
        request.session["report_table"] = grouped 
    else: 
        return HttpResponse("Not allowed")
    return HttpResponse(json.dumps(grouped),mimetype="application/json")

def new_report(rquest):
    departments = HaitiAdmin.objects.all()
    return render_to_response("damage-reports-new.html", 
                              {"departments" : departments})
