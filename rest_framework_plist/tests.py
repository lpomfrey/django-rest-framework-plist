# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import decimal
import datetime
from StringIO import StringIO
from django.test import TestCase
from django.utils import six
from rest_framework_plist.renderers import PlistRenderer
from rest_framework_plist.parsers import PlistParser


class PlistRendererTests(TestCase):
    '''
    Tests specific to the Plist Renderer
    '''

    def test_render_and_parse(self):
        '''
        Test rendering and then parsing returns the original object.
        i.e. obj -> render -> parse -> obj.
        '''
        obj = {'foo': ['bar', {'baz': [1, 2]}]}

        renderer = PlistRenderer()
        parser = PlistParser()

        content = renderer.render(obj, 'application/x-plist')
        data = parser.parse(StringIO(content))
        self.assertEquals(obj, data)

    def test_datetime(self):
        obj = {'my_datetime': datetime.datetime.now()}

        renderer = PlistRenderer()
        parser = PlistParser()

        content = renderer.render(obj, 'application/x-plist')
        data = parser.parse(StringIO(content))
        self.assertEquals(obj, data)

    def test_date(self):
        obj = {'my_date': datetime.date.today()}

        renderer = PlistRenderer()
        parser = PlistParser()

        content = renderer.render(obj, 'application/x-plist')
        data = parser.parse(StringIO(content))
        self.assertEquals(obj, data)

    def test_time(self):
        obj = {'my_time': datetime.datetime.now().time()}

        renderer = PlistRenderer()
        parser = PlistParser()

        content = renderer.render(obj, 'application/x-plist')
        data = parser.parse(StringIO(content))
        self.assertEquals(obj, data)

    def test_decimal(self):
        obj = {'my_decimal': decimal.Decimal(1) / decimal.Decimal(7)}

        renderer = PlistRenderer()
        parser = PlistParser()

        content = renderer.render(obj, 'application/x-plist')
        data = parser.parse(StringIO(content))
        self.assertEquals(obj, data)

    def test_none(self):
        obj = {'my_none': None}

        renderer = PlistRenderer()
        parser = PlistParser()

        content = renderer.render(obj, 'application/x-plist')
        data = parser.parse(StringIO(content))
        self.assertEquals(obj, data)

    def test_integer(self):
        obj = {'my_int': 1}

        renderer = PlistRenderer()
        parser = PlistParser()

        content = renderer.render(obj, 'application/x-plist')
        data = parser.parse(StringIO(content))
        self.assertEquals(obj, data)

    def test_unicode(self):
        if not six.PY3:
            chr = unichr
        obj = {'my_unicode': ''.join(chr(x) for x in range(2000))}

        renderer = PlistRenderer()
        parser = PlistParser()

        content = renderer.render(obj, 'application/x-plist')
        data = parser.parse(StringIO(content))
        self.assertEquals(obj, data)

        # ASCII only strings are represented as strings not data
        obj = {'my_unicode': 'abcdefghi'}

        renderer = PlistRenderer()
        parser = PlistParser()

        content = renderer.render(obj, 'application/x-plist')
        data = parser.parse(StringIO(content))
        self.assertEquals(obj, data)
