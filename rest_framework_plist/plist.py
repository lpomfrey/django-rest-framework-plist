# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import re
from decimal import Decimal
from plistlib import PlistWriter, PlistParser, Data

from biplist import readPlist, is_stream_binary_plist
from django.template.defaultfilters import escape
from django.utils import dateparse
from django.utils.encoding import smart_bytes, smart_text
from django.utils.six import BytesIO, text_type

try:  # pragma: no cover
    from HTMLParser import HTMLParser
except ImportError:  # pragma: no cover
    from html.parser import HTMLParser


_CONTROL_CHARS = re.compile(
    r'[\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0e\x0f\x10\x11\x12\x13'
    r'\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f]'
)


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
        value = h.unescape(smart_text(Data.fromBase64(self.getData()).data))
        if value == '\0':
            self.addObject(None)
        else:
            self.addObject(value)

    def end_string(self):
        h = HTMLParser()
        self.addObject(h.unescape(smart_text(self.getData())))


class RFPlistWriter(PlistWriter):
    '''
    A Plist writer that supports None type objects and has better datetime
    support
    '''

    def writeValue(self, value):
        DATETIME_TYPES = (datetime.datetime, datetime.date, datetime.time)
        if value is None:
            self.simpleElement(b'data', Data('\0').asBase64())
        elif isinstance(value, DATETIME_TYPES):
            self.simpleElement(b'date', smart_bytes(value.isoformat()))
        elif isinstance(value, Decimal):
            self.simpleElement(b'real', smart_bytes(value))
        elif isinstance(value, text_type):
            if _CONTROL_CHARS.search(value):
                # We can't represent the data as an ASCII string
                self.simpleElement(
                    b'data', Data(smart_bytes(escape(value))).asBase64())
            else:
                # Value can be represented as an ASCII string
                self.simpleElement(b'string', smart_bytes(escape(value)))
        else:
            PlistWriter.writeValue(self, value)


def read(stream):
    if not isinstance(stream, BytesIO):
        stream = BytesIO(stream)
    if is_stream_binary_plist(stream):
        return readPlist(stream)
    stream.seek(0)
    return RFPlistParser().parse(stream)


def write(data):
    writer = RFPlistWriter(BytesIO())
    writer.writeValue(data)
    return writer.file.getvalue()
