import cgi
from http.cookies import SimpleCookie
from urllib.parse import parse_qs

from ..request import Request
from ..utils import HeaderDict, cached_property


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
    def raw_cookies(self):
        '''Raw access to cookies'''
        cookie_data = self.environ.get('HTTP_COOKIE', '')
        cookies = SimpleCookie()
        if not cookie_data:
            return cookies
        cookies.load(cookie_data)
        return cookies

    @cached_property
    def cookies(self):
        '''Simplified Cookie access'''
        return {
            key: self.raw_cookies[key].value
            for key in self.raw_cookies.keys()
        }

    @cached_property
    def query(self):
        return parse_qs(
            self.environ.get('QUERY_STRING', ''),
            keep_blank_values=True
        )

    @property
    def content_type(self):
        if self._content_type is None:
            self._parse_content_type()
        return self._content_type

    @property
    def content_paras(self):
        if self._content_params is None:
            self._parse_content_type()
        return self._content_params

    def _parse_content_type(self):
        self._content_type, self._content_params = cgi.parse_header(self.environ.get('CONTENT_TYPE', ''))