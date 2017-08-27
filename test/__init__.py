from goonbag.wsgi import WsgiApplication
from goonbag import Routes, Handler

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


application = WsgiApplication(api)