from . import response


class Handler:
    default_status = 200
    default_content_type = 'text/html'

    def __init__(self, request):
        self.request = request

    def __call__(self, **kwargs):
        self.kwargs = kwargs
        return self.dispatch(self.request, **kwargs)

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
