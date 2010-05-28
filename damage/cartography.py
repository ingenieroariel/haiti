import httplib2
from urllib import urlencode

h = httplib2.Http(".cache")

class GeoServer(object):
    def __init__(self,url="http://localhost:8001/geoserver",version="1.1.1"):
        self.url = url
        self.version = version

    def get_map(self,layers=["haiti"],
                styles=[""],
                srs="EPSG:4326",
                bbox=[-75.9125,17.037095703125,-70.1865,20.984904296875],
                format="image/png",
                size=(300,300),
                transpartent=True,
                bgcolor="#fffff",
                method="GET",
                exceptions='application/vnd.ogc.se_xml'):         
        request = {"version": self.version,"request" : "GetMap","service" : "WMS"}
        request["width"] = str(size[0])
        request["height"] = str(size[1])
        request["layers"] = ",".join(layers) 
        request["styles"] = ",".join(styles)
        request["srs"] = str(srs)
        request["bbox"] = ','.join([str(x) for x in bbox])
        request["format"]= str(format)
        request["transparent"] = str(transpartent).upper()
        request["bgcolor"] = '0x' + bgcolor[1:7]
        request["exceptions"] = exceptions
        data = urlencode(request)
        resp, content = h.request("%s/wms?%s" % (self.url,data),method)
        return content



def make_sld(layers=None,version="1.1.1"):
    sld = ["<StyledLayerDescriptor version=\"1.0.0\">","</StyledLayerDescriptor>"]
    return "".join(sld)
    

def make_layer(name,style):
    return "".join(["<NamedLayer>",
            "<Name>",name,"</Name>",
            "<NamedStyle>",
            "<Name>",style,"</Name>",
            "</NamedStyle>",
            "</NamedLayer>"])
