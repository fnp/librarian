#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages


setup(
    name='librarian',
    version='1.2.5',
    description='Converter from WolneLektury.pl XML-based language to XHTML, TXT and other formats',
    author='Marek Stępniowski',
    author_email='marek@stepniowski.com',
    url='http://redmine.nowoczesnapolska.org.pl/',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=['lxml>=2.2'],
    scripts=['scripts/book2html', 'scripts/book2txt', 'scripts/bookfragments', 'scripts/genslugs'],
    tests_require=['nose>=0.11', 'coverage>=3.0.1'],
)
