import inspect

from .response import Response, InternalServerError


class Application:
    request_class = None

    def __init__(self, root, **config):
        self.root = root
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
