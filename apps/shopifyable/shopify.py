import base64
import urllib
import urllib2
import platform
import shopifyable

from shopifyable.utils import generate_url, generate_request, parse_json
import ssl
import httplib

import socket

class HTTPSConnectionV3(httplib.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)
        
    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if hasattr(self, '_tunnel_host') and self._tunnel_host:
            self.sock = sock
            self._tunnel()
        try:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_TLSv1)
        except ssl.SSLError, e:
            print("Trying SSLv3.")
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv23)
            
class HTTPSHandlerV3(urllib2.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(HTTPSConnectionV3, req)

class Shopify(object):
    DEFAULT_HEADERS = {
        'User-Agent':   'Shopipy/%s Python/%s %s/%s' % (shopifyable.__version__, platform.python_version(), platform.system(), platform.release()),
    }
    
    def __init__(self, domain, api_key, password, secure=True, api_throttle=None):
        self.protocol = "https" if secure else "http"
        self.domain = domain
        self.api_key = api_key
        self.api_throttle = api_throttle
        # HTTPBasicAuthHandler does not reliably set this header in Python 2.7
        # Originally, this code used a urllib2 urlopener.
        self.headers = dict(self.DEFAULT_HEADERS, **{
            "Authorization": "Basic %s" % base64.b64encode(":".join((api_key, password))),
        })
    
    def _request(self, method, path, get_params, body=None, headers={}):
        # Allow API throttling via various mechanisms
        if callable(self.api_throttle):
            self.api_throttle(self)
        
        # Create and send HTTP Request
        url = generate_url(self.protocol, self.domain, path, get_params)
        req_headers = dict(self.headers, **headers)
        #import rpdb2; rpdb2.start_embedded_debugger('0')
        request = generate_request(method, url, body)
        for name, value in req_headers.items():
            request.add_header(name, value)
        urllib2.install_opener(urllib2.build_opener(HTTPSHandlerV3()))

        conn = urllib2.urlopen(request)
        
        # Parse HTTP Response (expecting a well-formed XML document)
        root = parse_json(conn)
        return root
    
    def GET(self, path, **kwargs):
        """
        Issues an authenticated GET request to the given path
        If present, any keyword arguments are converted to GET parameters
        @return root - ElementTree root
        """
        return self._request('GET', path, kwargs)
    
    def POST(self, path, body, **kwargs):
        """
        Issues an authenticated POST request to the given path
        If present, any keyword arguments are converted to GET parameters
        @return root - ElementTree root
        """
        return self._request('POST', path, kwargs, body, headers = {
            'Content-Type': 'text/json',
        })
    
    def PUT(self, path, body, **kwargs):
        """
        Issues an authenticated PUT request to the given path
        If present, any keyword arguments are converted to GET parameters
        @return root - ElementTree root
        """
        return self._request('PUT', path, kwargs, body, headers = {
            'Content-Type': 'text/json',
        })
    
    def DELETE(self, path, **kwargs):
        """
        Issues an authenticated DELETE request to the given path
        If present, any keyword arguments are converted to GET parameters
        @return root - ElementTree root
        """
        return self._request('DELETE', path, kwargs)

