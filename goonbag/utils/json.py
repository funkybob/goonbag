
from ..handler import handler

try:
    import simplejson as json
except ImportError:
    import json


class returns_json(handler):
    '''
    Decorator to help for a handler which returns JSON
    '''
    content_type = 'application/json'

    def encode_response(self, resp):
        return json.dumps(resp)
