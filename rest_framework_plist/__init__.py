# -*- coding: utf-8 -*-
from distutils import version

__version__ = '0.3.0'
version_info = version.StrictVersion(__version__).version

from rest_framework_plist.parsers import PlistParser  # NOQA
from rest_framework_plist.renderers import PlistRenderer  # NOQA
