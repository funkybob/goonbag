import inspect

from .response import Response, InternalServerError


class Application:
    def __init__(self, routes, **config):
        self.routes = routes
        self.config = config

    def dispatch(self, match, request):
        handler = match.handler
        if inspect.isclass(handler):
            handler = handler(request)
        try:
            response = handler(request, **match.kwargs)
        except Response as resp:
            return resp
        except Exception as ex:
            # !! Raise 500 !!
            import traceback
            return InternalServerError(content=traceback.format_exc(ex))

        if isinstance(response, Response):
            return response

        if isinstance(response, str):
            return Response(200, response)
