#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import os
import os.path
from distutils.core import setup

def whole_tree(prefix, path):
    files = []
    for f in (f for f in os.listdir(os.path.join(prefix, path)) if not f[0]=='.'):
        new_path = os.path.join(path, f)
        if os.path.isdir(os.path.join(prefix, new_path)):
            files.extend(whole_tree(prefix, new_path))
        else:
            files.append(new_path)
    return files


setup(
    name='librarian',
    version='1.6',
    description='Converter from WolneLektury.pl XML-based language to XHTML, TXT and other formats',
    author="Marek Stępniowski",
    author_email='marek@stepniowski.com',
    maintainer='Radek Czajka',
    maintainer_email='radoslaw.czajka@nowoczesnapolska.org.pl',
    url='http://github.com/fnp/librarian',
    packages=['librarian', 'librarian.embeds'],
    package_data={'librarian': ['xslt/*.xslt', 'epub/*', 'mobi/*', 'pdf/*', 'fb2/*', 'fonts/*'] +
                                whole_tree(os.path.join(os.path.dirname(__file__), 'librarian'), 'res') +
                                whole_tree(os.path.join(os.path.dirname(__file__), 'librarian'), 'font-optimizer')},
    include_package_data=True,
    install_requires=[
        'lxml>=2.2',
        'Pillow',
    ],
    scripts=['scripts/book2html',
             'scripts/book2txt',
             'scripts/book2epub',
             'scripts/book2mobi',
             'scripts/book2pdf',
             'scripts/book2fb2',
             'scripts/book2partner',
             'scripts/book2cover',
             'scripts/bookfragments',
             'scripts/genslugs'],
    tests_require=['nose>=0.11', 'coverage>=3.0.1'],
)
