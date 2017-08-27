import parse
from collections import namedtuple

from .handler import Handler

# TODO:
# - nested routes
# - named rules
# - reverse


class RouteMatch(namedtuple('_RouteMatch', ('routes', 'pattern', 'handler', 'match'))):
    def dispatch(self, request):
        handler = self.handler
        if issubclass(handler, Handler):
            handler = handler()
        return handler(request, **self.match.named)


class Routes:
    def __init__(self):
        self.routes = []

    def build_parse(self, pattern):
        return parse.compile(pattern)

    def route(self, pattern):
        '''
        Decorator to add a new route to the list.

        @foo.route('/pattern/')
        def handler(request, ...)
        '''
        def _inner(handler):
            rule = (self.build_parse(pattern), handler)
            assert rule not in self.routes, 'Duplicate route: %r :> %r' % (pattern, handler)
            self.routes.append(rule)
            return handler

        return _inner

    def resolve(self, path):
        for pattern, handler in self.routes:
            m = pattern.parse(path)
            if m:
                return RouteMatch(self, pattern, handler, m)
        return None
