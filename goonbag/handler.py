from functools import update_wrapper, partial

from . import response
from .response import Response
from .utils import HeaderDict


class Handler:
    default_status = 200
    default_content_type = 'text/html'

    def __init__(self, request):
        self.request = request

    def __call__(self, request, **kwargs):
        self.kwargs = kwargs
        return self.dispatch(request, **kwargs)

    def dispatch(self, request, **kwargs):
        func = getattr(self, request.method.lower(), self.invalid_method)
        try:
            result = func(request, **kwargs)
        except response.Response as resp:
            return resp
        if isinstance(result, str):
            status = self.get_status(result)
            headers = self.get_headers(result)
            return self.make_response(status, result, headers)
        # ???

    def invalid_method(self, request, **kwargs):
        raise response.MethodNotAllowed([])

    def get_status(self, result):
        return self.default_status

    def get_headers(self, result):
        return {
            'Content-Type': self.default_content_type,
        }

    def make_response(self, status, result, headers):
        return response.Response(status, result, headers)


class handler:
    '''
    Decorator to help functions return responses
    '''
    encoding = 'utf-8'
    status = 200
    content_type = 'text/html'
    headers = None

    def __new__(cls, *args, **kwargs):
        if not args:
            return partial(cls, **kwargs)
        return super().__new__(cls)

    def __init__(self, func, status=None, content_type=None, headers=None):
        self.func = func
        if status is not None:
            self.status = status
        self.status = status
        if content_type:
            self.content_type = content_type
        if headers is None:
            headers = dict()
        headers.setdefault('Content-Type', self.content_type)
        self.headers = headers
        update_wrapper(self, func)

    def encode_response(self, resp):
        return resp.encode(self.encoding)

    def __call__(self, request, **kwargs):
        resp = self.func(request, **kwargs)
        if not isinstance(resp, Response):
            resp = self.encode_response(resp)
            resp = Response(self.status, resp, self.headers)
        return resp
