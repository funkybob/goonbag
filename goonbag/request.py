
import cgi
from http.cookies import SimpleCookie
from io import BytesIO

from .utils import cached_property
from .utils.json import json


class Request:
    method = None
    body = None
    query = None
    headers = None
    path = None

    @cached_property
    def raw_cookies(self):
        '''Raw access to cookies'''
        cookie_data = self.headers.get('Cookie', '')
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
    def post(self):
        body = BytesIO(self.body)
        return cgi.FieldStorage(body, self.headers, keep_blank_values=True)

    @cached_property
    def json(self):
        return json.loads(self.body)

    @property
    def content_type(self):
        if self._content_type is None:
            self._parse_content_type()
        return self._content_type

    @property
    def content_params(self):
        if self._content_params is None:
            self._parse_content_type()
        return self._content_params

    def _parse_content_type(self):
        self._content_type, self._content_params = cgi.parse_header(self.headers.get('Content-Type', ''))
