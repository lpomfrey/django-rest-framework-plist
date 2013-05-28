# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.parsers import BaseParser
from rest_framework.exceptions import ParseError
from rest_framework_plist.plist import read


class PlistParser(BaseParser):
    '''
    Parses Plist-serialized data.
    '''

    media_type = 'application/x-plist'

    def parse(self, stream, media_type=None, parser_context=None):
        try:
            return read(stream)
        except Exception as exc:
            raise ParseError('Plist parse error - {0}'.format(exc))
