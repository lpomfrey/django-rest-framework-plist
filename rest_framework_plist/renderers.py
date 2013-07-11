# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.renderers import BaseRenderer
from rest_framework_plist.plist import write


class PlistRenderer(BaseRenderer):
    '''
    Renderer which serializes to Plist.
    '''

    media_type = 'application/x-plist'
    format = 'plist'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        '''
        Renders ``data`` into serialized Plist.
        '''
        return write(data)
