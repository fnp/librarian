# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from zipfile import ZipFile
from lxml import html
from nose.tools import *
from librarian import DirDocProvider
from librarian.parser import WLDocument
from tests.utils import get_fixture


def test_transform():
    epub = WLDocument.from_file(
            get_fixture('text', 'asnyk_zbior.xml'),
            provider=DirDocProvider(get_fixture('text', ''))
        ).as_epub(flags=['without_fonts']).get_file()
    zipf = ZipFile(epub)

    # Check contributor list.
    last = zipf.open('OPS/last.html')
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
