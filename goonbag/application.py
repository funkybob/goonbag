from .http import Request


class Application:
    def __init__(self, routes):
        self.routes = routes

