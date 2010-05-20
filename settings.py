# Django settings for haiti project.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'          
DATABASE_NAME = 'haiti'             
DATABASE_USER = 'postgres'          
DATABASE_PASSWORD = ''         
DATABASE_HOST = ''             
DATABASE_PORT = ''             

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'
SEARCH_WIDGET_BASELAYER_INDEX = 0

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8egg+3%*(txbb4p#chvm+dnp7&mf-d@f8p!5(hif359zccfo^_'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)
MINIFIED_RESOURCES = False
GEOSERVER_CREDENTIALS = "admin", "geoserver"
GEOSERVER_BASE_URL = "http://localhost:8001/geoserver/"
DEFAULT_MAP_BASE_LAYER = "base:nic_admin"
DEFAULT_MAP_CENTER = [-84.7, 12.8]
DEFAULT_MAP_ZOOM = 7


ROOT_URLCONF = 'haiti.urls'

TEMPLATE_DIRS = ( 

#    "/home/ivan/Work/Haiti/haiti/templates",
#    "/home/ivan/Work/Haiti/src/geonodepy/geonode/templates"

    "/home/ivan/dev/Haiti/haiti/templates",
    "/home/ivan/dev/Haiti/src/geonodepy/geonode/templates"


)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'geonode.core',
    'geonode.maps',
    'geonode.proxy',
    'haiti.myhazard',
    'haiti.damage',

)
GOOGLE_API_KEY = "ABQIAAAAkofooZxTfcCv9Wi3zzGTVxTnme5EwnLVtEDGnh-lFVzRJhbdQhQgAhB1eT_2muZtc0dl-ZSWrtzmrw"
MAP_BASELAYERS = [{
        'service': "wms",
        'url': "http://maps.opengeo.org/geowebcache/service/wms?request=GetCapabilities",
        'layers': [
            'bluemarble'
        ]}, {
        'service': 'google',
        'apiKey' : GOOGLE_API_KEY,
        'layers': [
            'G_SATELLITE_MAP'
        ]}, {
        'service': "wms",
        'url': "%swms?request=GetCapabilities" % GEOSERVER_BASE_URL,
        'layers': [
            'base:CA'
        ]}
    ]

NAVBAR = \
{'community': {'id': '%sLink',
               'item_class': '',
               'link_class': '',
               'text': 'Contributed Maps',
               'url': 'geonode.views.community'},
 'curated': {'id': '%sLink',
             'item_class': '',
             'link_class': '',
             'text': 'CAPRA Maps',
             'url': 'geonode.views.curated'},
 'data': {'id': '%sLink',
          'item_class': '',
          'link_class': '',
          'text': 'Data',
          'url': "geonode.views.static page='data'"},
 'help': {'id': '%sLink',
          'item_class': '',
          'link_class': '',
          'text': 'Help',
          'url': "geonode.views.static page='help'"},
#  'index': {'id': '%sLink',
#            'item_class': '',
#            'link_class': '',
#            'text': 'Featured Map',
#            'url': 'geonode.views.index'},
 'master': {'id': '%sLink',
            'item_class': '',
            'link_class': '',
            'text': 'This page has no tab for this navigation'},
 'meta': {'active_class': 'here',
          'default_id': '%sLink',
          'default_item_class': '',
          'default_link_class': '',
          'end_class': 'last',
          'id': '%sLink',
          'item_class': '',
          'link_class': '',
          'visible': 'data\ncurated\ncommunity\nhelp'}}
if DEBUG:
    if MINIFIED_RESOURCES: 
        MEDIA_LOCATIONS = {
            "ext_base": "/static/ext/",
            "ol_theme": "/static/ol/theme/default/style.css",
            "ol_script":"/static/ol/OpenLayers.js",
            "gx_themes":"/static/gx/theme/",
            "gx_script":"/static/gx/GeoExt.js",
            "PrintPreview_script":"/static/PrintPreview/PrintPreview.js",
            "PrintPreview_themes": "/static/PrintPreview/theme/",
            "gxp_script":"/static/gxp/gxp.js",
            "gxp_theme":"/static/gxp/theme/all.css",
            "app_themes": "/static/gn/theme/app/",
            "app_script":"/static/gn/GeoNode.js",
            "ux_script":"/static/gn/ux.js",
        }                
    else:
        MEDIA_LOCATIONS = {
            "ext_base": "/static/externals/ext/",
            "ol_theme": "/static/externals/openlayers/theme/default/style.css",
            "ol_script":"/static/externals/openlayers/lib/OpenLayers.js",
            "gx_themes":"/static/externals/geoext/resources/",
            "gx_script":"/static/externals/geoext/lib/GeoExt.js",
            "PrintPreview_script":"/static/externals/PrintPreview/lib/GeoExt.ux/PrintPreview.js",
            "PrintPreview_themes": "/static/externals/PrintPreview/resources/",
            "gxp_script":"/static/externals/gxp/src/script/loader.js",
            "gxp_theme":"/static/externals/gxp/src/theme/all.css",
            "app_themes": "/static/src/theme/app/",
            "app_script":"/static/src/script/app/loader.js",
            "ux_script":"/static/src/script/ux/loader.js",
        }
else:
    MEDIA_LOCATIONS = {
        "ext_base": GEONODE_CLIENT_LOCATION + "/geonode-client/ext/",
        "ol_theme":  GEONODE_CLIENT_LOCATION + "/geonode-client/ol/theme/default/style.css",
        "ol_script": GEONODE_CLIENT_LOCATION + "/geonode-client/ol/OpenLayers.js",
        "gx_themes": GEONODE_CLIENT_LOCATION + "/geonode-client/gx/theme/",
        "gx_script": GEONODE_CLIENT_LOCATION + "/geonode-client/gx/GeoExt.js",
        "PrintPreview_script": GEONODE_CLIENT_LOCATION + "/geonode-client/PrintPreview/PrintPreview.js",
        "PrintPreview_themes": GEONODE_CLIENT_LOCATION + "/geonode-client/PrintPreview/theme/",
        "gxp_script": GEONODE_CLIENT_LOCATION + "/geonode-client/gxp/gxp.js",
        "gxp_theme": GEONODE_CLIENT_LOCATION + "/geonode-client/gxp/theme/all.css",
        "app_themes": GEONODE_CLIENT_LOCATION + "/geonode-client/gn/theme/app/",
        "app_script": GEONODE_CLIENT_LOCATION + "/geonode-client/gn/GeoNode.js",
        "ux_script": GEONODE_CLIENT_LOCATION + "/geonode-client/gn/ux.js",
    }



