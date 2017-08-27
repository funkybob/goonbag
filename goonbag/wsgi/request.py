from ..request import Request
from ..utils import HeaderDict


class WsgiRequest(Request):
    def __init__(self, environ):
        self.headers = HeaderDict(
            key[5:]: value
            for key, value in environ.items()
            if key.startswith('HTTP_')
        )
        self.META = environ