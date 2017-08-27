GOONBAG
=======

.. note::

  I am still looking for a better name than this. Come on, people, help me out
  here :)

- do work a most once
- use parse / format for url lookup / reverse
- use stencil?
- decorators are cool, ok?


.. code-block:: python

    from goonbag import Routes, Handler, handler
    from goonbag.utils.json import returns_json

    api = Routes()

    @api.route('/foo/{bar}/', ....)
    @handler
    def handler(request):
        ...
        return content: iterable


    @api.route('/baz/data')
    @returns_json
    def handler(request):
        ...
        return {...}


    @api.route('/baz/')
    class MyHandler(Handler):
        default_content_type = 'application/json'

        def get(self, request, \**url_params):
            return 'content'

Since routing uses `parse <https://pypi.org/project/parse/>`_ we can even cast
values on parse:

.. code-block:: python

    @api.route('/math/double/{value:d}')
    def double(request, value):
        # Value is already an int
        return str(value * 2)


To make a WSGI Application:

.. code-block:: python

    from goonbag.wsgi import WsgiApplication

    application = WsgiApplication(routes=api)

