import parse

from .response import NotFound

# TODO:
# - named rules
# - reverse
# - route arguments?


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

    def __call__(self, request):
        for pattern, handler in self.routes:
            m = pattern.parse(request.path)
            if m:
                return handler(request, **m.named)
        return NotFound()
