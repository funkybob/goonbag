from goonbag.utils.json import json


class SessionSerialiser:
    '''
    Mixin class for supporting different data serialising formats.
    '''
    def pack(self, data):
        raise NotImplementedError

    def unpack(self, data):
        raise NotImplementedError


class JsonSerialiser(SessionSerialiser):
    def pack(self, data):
        return json.dumps(data)

    def unpack(self, data):
        return json.loads(data)
