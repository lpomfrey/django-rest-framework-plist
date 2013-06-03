Django Rest Framework Plist
=============================

:Version: 0.2.0
:Author: Luke Pomfrey

Overview
========

This package provides `Plist <https://en.wikipedia.org/wiki/Property_list>`_ 
serialization  support for `Django REST framework 
<http://django-rest-framework.org>`_.

It is largely based on `the msgpack implementation
<https://github.com/juanriaza/django-rest-framework-msgpack>`_ by `Juan Riaza
<http://juanriaza.com/>`_.

Installation
============

Install using ``pip``:

.. code-block:: bash

    $ pip install djangorestframework-plist

...or clone the project from github:

.. code-block:: bash

    $ git clone git@github.com:lpomfrey/django-rest-framework-plist.git

Usage
=====

This package provides a renderer (``PlistRenderer``) and a parser (``PlistParser``).

See the REST framework documentation for details on enabling them:

- `Setting the renderer 
  <http://django-rest-framework.org/api-guide/renderers.html#setting-the-renderers>`_.
- `Setting the parser 
  <http://django-rest-framework.org/api-guide/parsers.html#setting-the-parsers>`_.


``rest_framework_plist.renderers.PlistRenderer``
---------------------------------------------------------

Renders the request data into ``Plist``.

:.media_type: ``application/x-plist``
:.format: ``.plist``

``rest_framework_plist.parsers.PlistParser``
---------------------------------------------------------

Parses ``Plist`` request content.

:.media_type: ``application/x-plist``


Running the tests
=================

To run the tests against the current environment::

    ./manage.py test

Changelog
=========

0.2.0
-----
**31st May 2013**

* Version bump

0.1.0
-----
**28th May 2013**

* Initial release
