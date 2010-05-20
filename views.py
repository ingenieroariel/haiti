from django.shortcuts import render_to_response
import simplejson as json
from django.conf import settings

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


def _split_query(query):
    """
    split and strip keywords, preserve space 
    separated quoted blocks.
    """

    qq = query.split(' ')
    keywords = []
    accum = None
    for kw in qq: 
        if accum is None: 
            if kw.startswith('"'):
                accum = kw[1:]
            elif kw: 
                keywords.append(kw)
        else:
            accum += ' ' + kw
            if kw.endswith('"'):
                keywords.append(accum[0:-1])
                accum = None
    if accum is not None:
        keywords.append(accum)
    return [kw.strip() for kw in keywords if kw.strip()]



DEFAULT_SEARCH_BATCH_SIZE = 10
MAX_SEARCH_BATCH_SIZE = 25
def metadata_search(request):
    """
    handles a basic search for data using the 
    GeoNetwork catalog.

    the search accepts: 
    q - general query for keywords across all fields
    start - skip to this point in the results
    limit - max records to return

    for ajax requests, the search returns a json structure 
    like this: 
    
    {
    'total': <total result count>,
    'next': <url for next batch if exists>,
    'prev': <url for previous batch if exists>,
    'query_info': {
        'start': <integer indicating where this batch starts>,
        'limit': <integer indicating the batch size used>,
        'q': <keywords used to query>,
    },
    'rows': [
      {
        'name': <typename>,
        'abstract': '...',
        'keywords': ['foo', ...],
        'detail' = <link to geonode detail page>,
        'attribution': {
            'title': <language neutral attribution>,
            'href': <url>
        },
        'download_links': [
            ['pdf', 'PDF', <url>],
            ['kml', 'KML', <url>],
            [<format>, <name>, <url>]
            ...
        ],
        'metadata_links': [
           ['text/xml', 'TC211', <url>],
           [<mime>, <name>, <url>],
           ...
        ]
      },
      ...
    ]}
    """
    if request.method == 'GET':
        params = request.GET
    elif request.method == 'POST':
        params = request.POST
    else:
        return HttpResponse(status=405)

    # grab params directly to implement defaults as
    # opposed to panicy django forms behavior.
    query = params.get('q', '')
    try:
        start = int(params.get('start', '0'))
    except:
        start = 0
    try:
        limit = min(int(params.get('limit', DEFAULT_SEARCH_BATCH_SIZE)),
                    MAX_SEARCH_BATCH_SIZE)
    except: 
        limit = DEFAULT_SEARCH_BATCH_SIZE

    advanced = {}
    bbox = params.get('bbox', None)
    if bbox:
        try:
            bbox = [float(x) for x in bbox.split(',')]
            if len(bbox) == 4:
                advanced['bbox'] =  bbox
        except:
            # ignore...
            pass

    result = _metadata_search(query, start, limit, **advanced)
    result['success'] = True
    return HttpResponse(json.dumps(result), mimetype="application/json")

def _metadata_search(query, start, limit, **kw):
    
    csw_url = "%ssrv/en/csw" % settings.GEONETWORK_BASE_URL
    csw = CatalogueServiceWeb(csw_url);

    keywords = _split_query(query)
    
    csw.getrecords(keywords=keywords, startposition=start+1, maxrecords=limit, bbox=kw.get('bbox', None))
    
    # build results 
    # join with django model to grab name and potentially other stuff...
    # XXX owslib discards result ordering     
    layers = dict([(layer.uuid, layer) for layer in Layer.objects.filter(uuid__in=csw.records.keys())])
    results = [_build_search_result(rec, layers.get(rec.identifier, None)) for rec in csw.records.values()]

    result = {'rows': results, 
              'total': csw.results['matches']}
    result['query_info'] = {
        'start': start,
        'limit': limit,
        'q': query
    }
    if start > 0: 
        prev = max(start - limit, 0)
        params = urlencode({'q': query, 'start': prev, 'limit': limit})
        result['prev'] = reverse('geonode.maps.views.metadata_search') + '?' + params

    next = csw.results.get('nextrecord', 0) 
    if next > 0:
        params = urlencode({'q': query, 'start': next - 1, 'limit': limit})
        result['next'] = reverse('geonode.maps.views.metadata_search') + '?' + params
    
    return result


def _build_search_result(rec, layer):
    """
    accepts an owslib.csw.CswRecord and 
    builds a POD structure representing 
    the search result.
    """
    result = {}
    result['title'] = rec.title
    result['abstract'] = rec.abstract
    result['keywords'] = [x for x in rec.subjects if x]
    
    # 
    # Take BBOX from GeoNetwork Result...
    # 
    # XXX Disabled until reliable srs info can be determined 
    # these almost all fail because the urns are 
    # not specific enough. 
    # 
    # if rec.bbox is not None:
    #     # transform bbox to EPSG:4326 (eh I think...)
    #     try:
    #         bbox_srs = gdal.SpatialReference(crs)
    #         out_srs = gdal.SpatialReference('EPSG:4326')
    #         ct = gdal.CoordTransform(bbox_srs, out_srs)
    #         pt0 = gdal.OGRGeometry('POINT(%s %s)' % (rec.bbox.minx, rec.bbox.miny))
    #         pt0.transform(ct)
    #         pt1 = gdal.OGRGeometry('POINT(%s %s)' % (rec.bbox.maxx, rec.bbox.maxy))
    #         pt1.transform(ct)
    #     
    #         result['bbox'] = {
    #             'minx': pt0.x,
    #             'miny': pt0.y,
    #             'maxx': pt1.x,
    #             'maxy': pt1.y
    #         }
    #     except:
    #         # oh well, garbage in, garbage out...
    #         pass
            
    if layer is None:
        # be semi-graceful with data that doesn't correspond
        # to a GeoNode layer...
        result['name'] = rec.identifier 
        result['detail'] = ''
        result['attribution'] = {'title': '', 'href': ''}
        result['download_links'] = []
        result['metadata_links'] = []
    else:
        result['name'] = layer.typename
        result['detail'] = reverse('geonode.maps.views.layerController', args=(layer.typename,))
        result['attribution'] = {'title': layer.publishing.attribution or '', 
                                 'href': layer.publishing.attribution_link or ''}    
        result['download_links'] = layer.download_links()
        result['metadata_links'] = layer.metadata_links

        bbox = layer.resource.latlon_bbox
        if bbox is not None:
            result['bbox'] = {
                'miny': bbox[0],
                'maxy': bbox[1],
                'minx': bbox[2],
                'maxx': bbox[3]
            }


    return result
    
    
def browse_data(request):
    # for non-ajax requests, render a generic search page
    return render_to_response('data_search.html', {
        'init_search': json.dumps(request.GET or {}),
        'background': json.dumps(settings.MAP_BASELAYERS[settings.SEARCH_WIDGET_BASELAYER_INDEX]),
        'GOOGLE_API_KEY' : settings.GOOGLE_API_KEY
    })


