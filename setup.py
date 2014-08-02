#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" weeplug – WeeChat scripts.

    Copyright ⓒ  2014 pyroscope <pyroscope.project@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import re

# Project name
name = 'weeplug'

# Support for http://python-distribute.org/distribute_setup.py
try:
    import distribute_setup
    distribute_setup.use_setuptools()
except:
    pass

try:
    from setuptools import setup, find_packages
except ImportError, exc:
    # from distutils.core import setup
    raise RuntimeError("'{0}' needs setuptools for installation ({1})".format(name, exc))

basedir = os.path.dirname(__file__)
srcfile = lambda *args: os.path.join(*((basedir,) + args))

expected = ('version', 'author', 'author_email', 'license', 'long_description')
project = {}
with open(srcfile('src', name, '__init__.py')) as handle:
    init_py = handle.read()
    project['long_description'] = re.search(r'^"""(.+?)^"""$', init_py, re.DOTALL|re.MULTILINE).group(1).strip()
    for line in init_py.splitlines():
        match = re.match(r"""^__({0})__ += (?P<q>['"])(.+?)(?P=q)$""".format('|'.join(expected)), line)
        if match:
            project[match.group(1)] = match.group(3)

if not all(i in project for i in expected):
    raise RuntimeError("Missing or bad metadata in '{0}' package".format(name))

with open(srcfile('requirements.txt'), 'r') as handle:
    requires = [i.strip() for i in handle if i.strip() and not i.startswith('#')]

#with open(srcfile('test-requirements.txt'), 'r') as handle:
#    test_requires = [i.strip() for i in handle if i.strip() and not i.startswith('#')]

project.update(dict(
    name = name,
    description = project['long_description'].split('.')[0],
    url = 'https://github.com/pyroscope/weeplug',
    package_dir = {'': 'src'},
    packages = find_packages(srcfile('src'), exclude=['tests']),
    zip_safe = True,
    include_package_data = True,
    install_requires = requires,
    #setup_requires = ...,
    #test_suite = 'nose.collector',
    #test_suite = 'tests',
    #tests_require = test_requires,
    #extras_require = {'test': test_requires},
    classifiers = (
        # See http://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 3 - Alpha',
        'Environment :: Console :: Curses',
        'Environment :: Plugins',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
    ),
))

if __name__ == '__main__':
    setup(**project)
