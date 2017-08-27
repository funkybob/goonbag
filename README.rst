GOONBAG
=======

- do work a most once
- use parse / format for url lookup / reverse
- use stencil?
- decorators are cool, ok?


api = Routes()

@api.route('/foo/{bar}/', ....)
@responds(status=200, content_type='application/json')
def handler(request):
    ...
    return content: iterable

    return status:int, content: iterable

    return status:int, content: iterable, headers:dict


@api.route('/baz/')
class MyHandler(Handler):
    default_content_type = 'application/json'

    def get(self, request, \**url_params):
        return 'content'

