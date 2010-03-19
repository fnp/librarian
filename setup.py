#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
from tests.utils import TestCommand

setup(
    name='librarian',
    version='1.2.1',
    description='Converter from WolneLektury.pl XML-based language to XHTML, TXT and other formats',
    author='Marek Stępniowski',
    author_email='marek@stepniowski.com',
    url='http://redmine.nowoczesnapolska.org.pl/',
    packages=['librarian', 'tests'],
    package_dir={'librarian': 'librarian', 'tests': 'tests'},
    package_data={
        'librarian': ['*.xslt'],
        'tests': ['files/dcparser/*.xml', 'files/erroneous/*.xml'],
    },
    scripts=['scripts/book2html', 'scripts/book2txt', 'scripts/bookfragments', 'scripts/genslugs'],
    cmdclass={'test': TestCommand},
)
