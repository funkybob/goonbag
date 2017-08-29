
from . import Session


class SessionStorage:
    def new(self):
        key = self.make_key()
        return Session(key)

    def get(self, key):
        raise NotImplementedError

    def save(self, session):
        raise NotImplementedError


class RedisStorage(SessionStorage):
    def __init__(self, host='localhost', port=6379, db=0, prefix=''):
        try:
            import redis
        except ImportError:
            log.error('You must install the "redis" package to use RedisStorage.')
            raise
        self.prefix = prefix
        self.conn = redis.StrictRedis(host=host, port=port, db=db)

    def make_key(self, key):
        if not self.prefix:
            return key
        return '-'.join([self.prefix, key])

    def get(self, key):
        data = self.conn.get(self.make_key(key))
        return self.unpack(data)

    def set(self, session):
        data = self.pack(session)
        self.conn.set(self.make_key(key), data)
