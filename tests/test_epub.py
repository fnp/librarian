# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from __future__ import unicode_literals

import subprocess
from zipfile import ZipFile
from ebooklib import epub
from lxml import html
from nose.tools import *
from librarian import DirDocProvider
from librarian.parser import WLDocument
from tests.utils import get_fixture


def test_transform():
    epub_file = WLDocument.from_file(
            get_fixture('text', 'asnyk_zbior.xml'),
            provider=DirDocProvider(get_fixture('text', ''))
        ).as_epub(cover=True, flags=['without_fonts'])
    zipf = ZipFile(epub_file.get_file())

    # Check contributor list.
    last = zipf.open('EPUB/last.xhtml')
    tree = html.parse(last)
    editors_attribution = False
    for par in tree.findall("//p"):
        if par.text.startswith(u'Opracowanie redakcyjne i przypisy:'):
            editors_attribution = True
            assert_equal(
                par.text.rstrip(),
                u'Opracowanie redakcyjne i przypisy: '
                u'Adam Fikcyjny, Aleksandra Sekuła, Olga Sutkowska.')
    assert_true(editors_attribution)

    # Check that we have a valid EPUB.
    assert_equal(
        subprocess.call([
            'epubcheck', '-quiet', epub_file.get_filename()
        ]),
        0
    )

    book = epub.read_epub(epub_file.get_filename())

    # Check that guide items are there.
    assert_equals(
        book.guide,
        [
            {'href': 'part1.xhtml', 'title': 'Początek', 'type': 'text'},
            {'href': 'cover.xhtml', 'title': 'Okładka', 'type': 'cover'}
        ]
    )

    # Check that metadata is there.
    DC = "http://purl.org/dc/elements/1.1/"
    OPF = "http://www.idpf.org/2007/opf"

    assert_equals(
        book.get_metadata(OPF, "cover"),
        [(None, {'name': 'cover', 'content': 'cover-img'})]
    )
    assert_equals(
        book.get_metadata(DC, "title"),
        [('Poezye', {})]
    )
    assert_equals(
        book.get_metadata(DC, "language"),
        [('pl', {})]
    )
    assert_equals(
        book.get_metadata(DC, "identifier"),
        [('http://wolnelektury.pl/katalog/lektura/poezye', {
            'id': 'id',
        })]
    )
    assert_equals(
        book.get_metadata(DC, "creator"),
        [('Adam Asnyk', {"id": "creator"})]
    )
    assert_equals(
        book.get_metadata(DC, "publisher"),
        [('Fundacja Nowoczesna Polska', {})]
    )
    assert_equals(
        book.get_metadata(DC, "date"),
        [("2007-09-06", {})]
    )


def test_transform_hyphenate():
    epub = WLDocument.from_file(
            get_fixture('text', 'asnyk_zbior.xml'),
            provider=DirDocProvider(get_fixture('text', ''))
        ).as_epub(
            flags=['without_fonts'],
            hyphenate=True
        ).get_file()
