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


application = WsgiApplication(api)