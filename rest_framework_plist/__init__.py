# -*- coding: utf-8 -*-
from distutils import version

__version__ = '0.2.2'
version_info = version.StrictVersion(__version__).version

from .parsers import PlistParser  # NOQA
from .renderers import PlistRenderer  # NOQA
