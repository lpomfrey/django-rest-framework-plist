Django Rest Framework Plist
=============================

`Plist <https://en.wikipedia.org/wiki/Property_list>`_ serialization support 
for `Django REST framework <http://django-rest-framework.org>`_.

.. image:: https://badge.fury.io/py/djangorestframework-plist.png
    :target: http://badge.fury.io/py/djangorestframework-plist

.. image:: https://travis-ci.org/lpomfrey/django-rest-framework-plist.png?branch=master
    :target: https://travis-ci.org/lpomfrey/django-rest-framework-plist

.. image:: https://coveralls.io/repos/lpomfrey/django-rest-framework-plist/badge.png?branch=master
    :target: https://coveralls.io/r/lpomfrey/django-rest-framework-plist?branch=master

Installation
------------

Install using ``pip``:

.. code-block:: bash

    $ pip install djangorestframework-plist

...or clone the project from github:

.. code-block:: bash

    $ git clone git@github.com:lpomfrey/django-rest-framework-plist.git

Usage
-----

This package provides a renderer (``rest_framework_plist.PlistRenderer``) and a 
parser (``rest_framework_plist.PlistParser``).

Add the renderer and/or parser provided by this package to your settings, as 
described in the django-rest-framework documentation:

- `Setting the renderer 
  <http://django-rest-framework.org/api-guide/renderers.html#setting-the-renderers>`_.
- `Setting the parser 
  <http://django-rest-framework.org/api-guide/parsers.html#setting-the-parsers>`_.


+----------------------------------------+-------------------------+
| ``rest_framework_plist.renderers.PlistRenderer``                 |
+========================================+=========================+
| Renders the request data into ``Plist``.                         |
+----------------------------------------+-------------------------+
| .media_type                            | ``application/x-plist`` |
+----------------------------------------+-------------------------+
| .format                                | ``plist``               |
+----------------------------------------+-------------------------+

+----------------------------------------+-------------------------+
| ``rest_framework_plist.parsers.PlistParser``                     |
+========================================+=========================+
| Parses ``Plist`` request content.                                |
+----------------------------------------+-------------------------+
| .media_type                            | ``application/x-plist`` |
+----------------------------------------+-------------------------+
