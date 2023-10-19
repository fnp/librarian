#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import os
import os.path
from setuptools import setup, find_packages


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
    version='23.10',
    description='Converter from WolneLektury.pl XML-based language to XHTML, TXT and other formats',
    author="Marek Stępniowski",
    author_email='marek@stepniowski.com',
    maintainer='Radek Czajka',
    maintainer_email='radekczajka@wolnelektury.pl',
    url='http://github.com/fnp/librarian',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={'librarian': ['xslt/*.xslt', 'pdf/*', 'fb2/*', 'fonts/*'] +
                                whole_tree(os.path.join(os.path.dirname(__file__), 'src/librarian'), 'res') +
                                whole_tree(os.path.join(os.path.dirname(__file__), 'src/librarian'), 'locale')},
    include_package_data=True,
    install_requires=[
        'lxml>=2.2,<5.0',
        'Pillow>=9.1.0',
        'texml',
        'ebooklib',
        'aeneas',
        'mutagen',
        'qrcode',
        'requests',
        'fonttools',
    ],
    entry_points = {
        "console_scripts": [
            "librarian=librarian.command_line:main"
        ]
    },
    scripts=['scripts/book2html',
             'scripts/book2txt',
             'scripts/book2pdf',
             'scripts/book2fb2',
             'scripts/book2cover',
             ],
)
