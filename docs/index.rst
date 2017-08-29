Goonbag
=======

.. rubric: Looking for a better name since ... forever.

What?
=====

It's a web nano-framework.

Why?
----

After using Flask and similar tools for my clients, I didn't like their
approach of sticking things magically into globals.  Thread locals I can
understand, but globals I don't want.

Getting Started
===============

So, you want to write a simple web API.

Let's start with a basic request handler, and a URL router. URL routing is done
using `parse <https://pypi.org/project/parse/>`_ syntax.

.. code-block:: python

   from goonbag import handler, Routes

   api = Routes()

   @api.route('/')
   @handler
   def index(requet):
       return 'Welcome!'


Simple, but it doesn't really do anything - yet.

Next we need to create an ``Application`` to run this.  In this cae, we'll make
a WSGI Application.


.. code-block:: python

   from goonbag.wsgi import WsgiApplication

   ...

   application = WsgiApplication(routes)

Now you can launch your application with, for instance, `uWSGI
<http://uwsgi-docs.readthedocs.io>`_ :

.. code-block:: sh

   uwsgi --http-socket :8000 --python-path `pwd` --module myapp


Go to http://localhost:8000/ and you should be greeted with a friendly
`Welcome!`

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
