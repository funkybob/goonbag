
from ..application import Application
from .request import WsgiRequest


class WsgiApplication(Application):
    def __call__(self, env, start_response):
        request = WsgiRequest(env)

        path = env.get('PATH_INFO', b'/')

        route_match = self.routes.resolve(path)
        if route_match is None:
            # 404!
            start_response('400 Not Found', [])
            return []

        response = self.dispatch(route_match, request)

        start_response(response.status, response.headers.items())
        return iter(response)
