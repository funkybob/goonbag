
from ..application import Application
from .request import WsgiRequest


class WsgiApplication(Application):
    encoding = 'utf-8'

    def __call__(self, env, start_response):
        request = WsgiRequest(env)

        response = self.dispatch(self.routes, request)

        start_response(response.status, response.headers.items())

        value = response.content
        if not hasattr(value, '__iter__') or isinstance(value, (bytes, str)):
            value = [value]

        for chunk in value:
            # Don't encode when already bytes or Content-Encoding set
            yield chunk if isinstance(chunk, bytes) else chunk.encode(self.encoding)
