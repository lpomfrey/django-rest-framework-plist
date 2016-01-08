# -*- coding: utf-8 -*-

import datetime
from decimal import Decimal
from plistlib import Data, PlistParser, PlistWriter

from biplist import is_stream_binary_plist, readPlist
from django.template.defaultfilters import escape
from django.utils import dateparse, six
from django.utils.encoding import force_bytes, force_text
from django.utils.six.moves.html_parser import HTMLParser


class RFPlistParser(PlistParser):
    '''
    A Plist parser that correctly handles timezones on dates
    '''

    def end_date(self):
        value = self.getData()
        if dateparse.parse_datetime(value) is not None:
            self.addObject(dateparse.parse_datetime(value))
        elif dateparse.parse_date(value) is not None:
            self.addObject(dateparse.parse_date(value))
        elif dateparse.parse_time(value) is not None:
            self.addObject(dateparse.parse_time(value))
        else:
            raise ValueError('"{0}" is not a valid datetime'.format(value))

    def end_real(self):
        self.addObject(Decimal(self.getData()))

    def end_data(self):
        h = HTMLParser()
        value = h.unescape(force_text(Data.fromBase64(self.getData()).data))
        self.addObject(value)

    def end_string(self):
        h = HTMLParser()
        data = h.unescape(force_text(self.getData()))
        if data == '__PyNone__':
            self.addObject(None)
        else:
            self.addObject(data)


class RFPlistWriter(PlistWriter):
    '''
    A Plist writer that supports ``None`` type objects and has better datetime
    support
    '''

    def writeValue(self, value):
        DATETIME_TYPES = (datetime.datetime, datetime.date, datetime.time)
        if isinstance(value, DATETIME_TYPES):
            self.simpleElement('date', value.isoformat())
        elif isinstance(value, Decimal):
            self.simpleElement(
                'real',
                force_text(value) if six.PY3 else force_bytes(value)
            )
        elif isinstance(value, (six.text_type, six.binary_type)):
            try:
                data = escape(value)
                if six.PY3:
                    data = force_text(data)
                else:
                    data = force_bytes(data)
                self.simpleElement('string', data)
            except ValueError as e:
                if 'contains control characters' in e.args[0]:
                    data = Data(force_bytes(escape(value))).asBase64()
                    if six.PY3:
                        data = force_text(data)
                    self.simpleElement('data', data)
                else:
                    raise
        elif value is None:
            self.simpleElement('string', '__PyNone__')
        elif value:
            PlistWriter.writeValue(self, value)


def read(stream):
    if not isinstance(stream, six.BytesIO):
        stream = six.BytesIO(stream)
    if is_stream_binary_plist(stream):
        stream.seek(0)
        return readPlist(stream)
    stream.seek(0)
    return RFPlistParser().parse(stream)


def write(data):
    writer = RFPlistWriter(six.BytesIO())
    writer.writeValue(data)
    return writer.file.getvalue()
