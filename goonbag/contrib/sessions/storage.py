

class SessionStorage:
    def new(self):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def save(self, session):
        raise NotImplementedError
