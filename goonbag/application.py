import inspect

from .response import Response, InternalServerError


class Application:
    def __init__(self, routes, **config):
        self.routes = routes
        self.config = config

    def dispatch(self, handler, request):
        if inspect.isclass(handler):
            handler = handler(request)
        try:
            return handler(request)
        except Response as resp:
            return resp
        except Exception as ex:
            # !! Raise 500 !!
            import traceback
            return InternalServerError(content=traceback.format_exc(ex))
