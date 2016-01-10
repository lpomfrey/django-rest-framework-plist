# -*- coding: utf-8 -*-

import datetime
import plistlib
from decimal import Decimal
from functools import partial

import biplist
from django.utils import dateparse, six
from django.utils.encoding import force_text
from django.utils.six.moves.html_parser import HTMLParser


DATETIME_TYPES = (datetime.datetime, datetime.date, datetime.time)


if hasattr(plistlib, 'dumps') and hasattr(plistlib, 'loads'):

    loads = plistlib.loads
    dumps = partial(plistlib.dumps, fmt=plistlib.FMT_BINARY)

else:

    class RFPlistParser(plistlib.PlistParser):
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
            value = h.unescape(force_text(
                plistlib.Data.fromBase64(self.getData()).data
            ))
            self.addObject(value)

        def end_string(self):
            h = HTMLParser()
            data = h.unescape(force_text(self.getData()))
            if data == '__PyNone__':
                self.addObject(None)
            else:
                self.addObject(data)

    def loads(stream):
        return RFPlistParser().parse(stream)

    def dumps(data):
        return biplist.writePlistToString(data)


def read(stream):
    if not isinstance(stream, six.BytesIO):
        stream = six.BytesIO(stream)
    if biplist.is_stream_binary_plist(stream):
        stream.seek(0)
        return biplist.readPlist(stream)
    stream.seek(0)
    return loads(stream)


def write(data):

    def _clean(obj):
        if isinstance(obj, DATETIME_TYPES):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {k: _clean(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [_clean(o) for o in obj]
        elif isinstance(obj, Decimal):
            return float(obj)
        else:
            return obj

    return dumps(_clean(data))
