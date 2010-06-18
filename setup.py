#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from distutils.core import setup

setup(
    name='librarian',
    version='1.3',
    description='Converter from WolneLektury.pl XML-based language to XHTML, TXT and other formats',
    author="Marek Stępniowski",
    author_email='marek@stepniowski.com',
    maintainer='Łukasz Rekucki',
    maintainer_email='lrekucki@gmail.com',
    url='http://github.com/fnp/librarian',
    packages=['librarian'],
    package_data={'librarian': ['xslt/*.xslt']},
    include_package_data=True,
    install_requires=['lxml>=2.2'],
    scripts=['scripts/book2html',
             'scripts/book2txt',
             'scripts/bookfragments',
             'scripts/genslugs'],
    tests_require=['nose>=0.11', 'coverage>=3.0.1'],
)
