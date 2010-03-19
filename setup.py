#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='librarian',
    version='1.3',
    description='Converter from WolneLektury.pl XML-based language to XHTML, TXT and other formats',
    author="Marek Stępniowski",
    author_email='marek@stepniowski.com',
    mantainer='Łukasz Rekucki',
    mantainer_email='lrekucki@gmail.com',
    url='http://github.com/fnp/librarian',    
    packages=['librarian'],
    package_data = {'librarian': ['xslt/*.xslt']},
    include_package_data=True,
    install_requires=['lxml>=2.2'],
    scripts=['scripts/book2html', 
             'scripts/book2txt', 
             'scripts/bookfragments', 
             'scripts/genslugs'],
             
    tests_require=['nose>=0.11', 'coverage>=3.0.1'],
)
