from http.cookies import SimpleCookie

from .utils import cached_property
from .utils.json import json


class Request:
    method = None
    body = None
    query = None
    headers = None
    path = None
    content_type = None
    content_params = None

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
    def json(self):
        return json.loads(self.body)
