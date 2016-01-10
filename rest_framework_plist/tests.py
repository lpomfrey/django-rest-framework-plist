# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import decimal
import datetime

from biplist import writePlistToString
from django.test import TestCase
from django.utils import six
from rest_framework_plist.renderers import PlistRenderer
from rest_framework_plist.parsers import PlistParser


if not six.PY3:
    chr = unichr


class PlistTests(TestCase):
    '''
    Tests specific to the Plist Renderer and Parser
    '''

    def setUp(self):
        self.renderer = PlistRenderer()
        self.parser = PlistParser()

    def _check_round_trip(self, obj, **kwargs):
        expected = kwargs.pop('expected', obj)
        content = self.renderer.render(obj, 'application/x-plist')
        data = self.parser.parse(content)
        self.assertEquals(expected, data)

    def test_render_and_parse(self):
        '''
        Test rendering and then parsing returns the original object.
        i.e. obj -> render -> parse -> obj.
        '''
        obj = {'foo': ['bar', {'baz': [1, 2]}]}
        self._check_round_trip(obj)

    def test_datetime(self):
        obj = {'my_datetime': datetime.datetime.now()}
        self._check_round_trip(
            obj, expected={'my_datetime': obj['my_datetime'].isoformat()}
        )

    def test_date(self):
        obj = {'my_date': datetime.date.today()}
        self._check_round_trip(
            obj, expected={'my_date': obj['my_date'].isoformat()}
        )

    def test_time(self):
        obj = {'my_time': datetime.datetime.now().time()}
        self._check_round_trip(
            obj, expected={'my_time': obj['my_time'].isoformat()}
        )

    def test_decimal(self):
        obj = {'my_decimal': decimal.Decimal(1) / decimal.Decimal(7)}
        self._check_round_trip(
            obj, expected={'my_decimal': float(obj['my_decimal'])}
        )

    def test_none(self):
        obj = {'my_none': None}
        self._check_round_trip(obj)

    def test_integer(self):
        obj = {'my_int': 1}
        self._check_round_trip(obj)

    def test_unicode(self):
        chars = [chr(x) for x in range(2000)]
        obj = {'my_unicode': ''.join(chars)}
        self._check_round_trip(obj)

        # ASCII only strings are represented as strings not data
        obj = {'my_unicode': 'abcdefghi'}
        self._check_round_trip(obj)

    def test_parse_binary_plist(self):
        obj = {
            'date': datetime.datetime.now().replace(microsecond=0),
            'int': 1,
            'real': 2.0,
            'none': None,
            'string': 'abc',
        }
        binary = writePlistToString(obj)
        data = self.parser.parse(binary)
        self.assertEqual(data, obj)
