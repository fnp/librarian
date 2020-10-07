# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from __future__ import unicode_literals

import io
from unittest import TestCase
from librarian import NoDublinCore
from librarian.document import WLDocument
from librarian.parser import WLDocument as LegacyWLDocument
from nose.tools import *
from .utils import get_fixture


class TransformTest(TestCase):
    maxDiff = None

    def test_transform_legacy(self):
        expected_output_file_path = get_fixture('text', 'asnyk_miedzy_nami_expected.legacy.html')

        html = LegacyWLDocument.from_file(
            get_fixture('text', 'miedzy-nami-nic-nie-bylo.xml')
        ).as_html().get_bytes().decode('utf-8')

        self.assertEqual(html, io.open(expected_output_file_path).read())

    def test_transform(self):
        expected_output_file_path = get_fixture('text', 'asnyk_miedzy_nami_expected.html')
        html = WLDocument(
            filename=get_fixture('text', 'miedzy-nami-nic-nie-bylo.xml')
        ).build('html').get_bytes().decode('utf-8')

        self.assertEqual(html, io.open(expected_output_file_path).read())


@raises(NoDublinCore)
def test_no_dublincore():
    LegacyWLDocument.from_file(
            get_fixture('text', 'asnyk_miedzy_nami_nodc.xml')
        ).as_html()


def test_passing_parse_dublincore_to_transform():
    """Passing parse_dublincore=False to transform omits DublinCore parsing."""
    LegacyWLDocument.from_file(
            get_fixture('text', 'asnyk_miedzy_nami_nodc.xml'),
            parse_dublincore=False,
        ).as_html()


def test_empty():
    assert not LegacyWLDocument.from_bytes(
            b'<utwor />',
            parse_dublincore=False,
        ).as_html()
