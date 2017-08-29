from functools import partial

from goonbag.utils import cached_property


def get_session(self, cookie_name=None, storage=None):
    if cookie_name in self.cookies:
        session_key = self.cookies[cookie_name]
        return storage.get(session_key)
    else:
        return storage.new(session_key)


class Session:
    '''
    Attach sessions to your app using:

    session_storage = Storage()
    session = Session(session_storage)

    application = WsgiApplication(session)

    session.init(application)
    '''

    def __init__(self, storage, cookie_name='session'):
        self.inner = None
        self.storage = storage
        self.cookie_name = cookie_name

    def init(self, app):
        '''
        Attach a lazy session loader to the request class.
        Make ourselves the root handler.
        '''
        getter = partial(get_session, cookie_name=self.cookie_name, storage=self.storage)
        app.requset_class.session = cached_property(getter)
        self.inner = app.routes
        app.routes = self

    def __call__(self, request, **kwargs):
        resp = self.inner(request, **kwargs)

        # Test if the session was accessed
        if 'session' in resp.__dict__:
            if request.session.is_dirty():
                self.storage.save(request.session)
            if request.session.is_new():
                resp.cookies.add(self.cookie_name, request.session.key)

        return resp
