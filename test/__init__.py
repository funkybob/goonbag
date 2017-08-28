from goonbag.wsgi import WsgiApplication
from goonbag import Routes, Handler, handler

api = Routes()


@api.route('/')
@handler
def index(request):
    return 'Welcome!'


@api.route('/greet')
class Greet(Handler):
    def get(self, request):
        return 'Hello, {}'.format(request.query.get('name', 'friend'))


@api.route('/double/{number:d}')
@handler
def double(request, number):
    return str(number * 2)


@api.route('/get/json/')
@handler.json
def json_endpoint(request):
    return {
        'data': [1, 2, 3],
        'errors': None,
    }

application = WsgiApplication(api)
