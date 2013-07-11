#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
from setuptools import setup


def get_version(package):
    '''
    Return package version as listed in `__version__` in `init.py`.
    '''
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search(
        '^__version__ = [\'"]([^\'"]+)[\'"]', init_py, re.MULTILINE
    ).group(1)


def get_packages(package):
    '''
    Return root package and all sub-packages.
    '''
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    '''
    Return all files under the root package, that are not in a
    package themselves.
    '''
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


version = get_version('rest_framework_plist')


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    args = {'version': version}
    print 'You probably want to also tag the version now:'
    print ' git tag -a release/{version} -m \'version {version}\''.format(**args)
    print ' git push --tags'
    sys.exit()


setup(
    name='djangorestframework-plist',
    version=version,
    url='http://github.com/lpomfrey/django-rest-framework-plist',
    license='BSD',
    description='Plist support for Django REST framework',
    author='Luke Pomfrey',
    author_email='lpomfrey@gmail.com',
    packages=get_packages('rest_framework_plist'),
    package_data=get_package_data('rest_framework_plist'),
    install_requires=open('requirements.txt').read().split('\n'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP'
    ]
)
