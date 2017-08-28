
import cgi
from urllib.parse import parse_qs

from ..request import Request
from ..utils import HeaderDict, cached_property
from ..utils.json import json


class WsgiRequest(Request):
    _content_type = None
    _content_params = None

    def __init__(self, environ):
        self.environ = environ
        self.method = environ.get('REQUEST_METHOD')
        self.path = environ.get('PATH_INFO', b'/')
        self.headers = HeaderDict(
            (key[5:], value)
            for key, value in environ.items()
            if key.startswith('HTTP_')
        )
        self.META = environ

    @cached_property
    def body(self):
        size = int(self.environ.get('CONTENT_LENGTH', 0))
        if not size:
            return ''
        return self.environ['wsgi.input'].read(size)

    @cached_property
    def post(self):
        return cgi.FieldStorage(self.environ['wsgi.input'], self.headers, keep_blank_values=True)

    @cached_property
    def json(self):
        return json.load(self.environ['wsgi.input'])

    @cached_property
    def query(self):
        return parse_qs(
            self.environ.get('QUERY_STRING', ''),
            keep_blank_values=True
        )

    def _parse_content_type(self):
        self._content_type, self._content_params = cgi.parse_header(self.environ.get('CONTENT_TYPE', ''))
