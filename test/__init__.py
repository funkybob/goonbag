from goonbag.wsgi import WsgiApplication
from goonbag import Routes, Handler
from goonbag.utils.json import returns_json

api = Routes()


@api.route('/')
def index(request):
    return 'Welcome!'


@api.route('/greet')
class Greet(Handler):
    def get(self, request):
        return 'Hello, {}'.format(request.query.get('name', 'friend'))


@api.route('/double/{number:d}')
def double(request, number):
    return str(number * 2)


@api.route('/get/json/')
@returns_json
def json_endpoint(request):
    return {
        'data': [1, 2, 3],
        'errors': None,
    }

application = WsgiApplication(api)