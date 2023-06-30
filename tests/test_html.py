# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import re
from unittest import TestCase
from librarian import NoDublinCore
from librarian.builders import builders
from librarian.document import WLDocument
from librarian.parser import WLDocument as LegacyWLDocument
from .utils import get_fixture


class TransformTest(TestCase):
    maxDiff = None

    def test_transform_legacy(self):
        expected_output_file_path = get_fixture('text', 'asnyk_miedzy_nami_expected.legacy.html')

        html = LegacyWLDocument.from_file(
            get_fixture('text', 'miedzy-nami-nic-nie-bylo.xml')
        ).as_html().get_bytes().decode('utf-8')

        html = re.sub(r'idm\d+', 'idmNNN', html)
        with open(expected_output_file_path) as f:
            self.assertEqual(f.read(), html)

    def test_transform(self):
        expected_output_file_path = get_fixture('text', 'asnyk_miedzy_nami_expected.html')
        html = WLDocument(
            filename=get_fixture('text', 'miedzy-nami-nic-nie-bylo.xml')
        ).build(builders['html']).get_bytes().decode('utf-8')

        with open(expected_output_file_path) as f:
            self.assertEqual(html, f.read())

    def test_no_dublincore(self):
        with self.assertRaises(NoDublinCore):
            LegacyWLDocument.from_file(
                get_fixture('text', 'asnyk_miedzy_nami_nodc.xml')
            ).as_html()

    def test_passing_parse_dublincore_to_transform(self):
        """Passing parse_dublincore=False to transform omits DublinCore parsing."""
        LegacyWLDocument.from_file(
            get_fixture('text', 'asnyk_miedzy_nami_nodc.xml'),
            parse_dublincore=False,
        ).as_html()

    def test_empty(self):
        self.assertIsNone(
            LegacyWLDocument.from_bytes(
                b'<utwor />',
                parse_dublincore=False,
            ).as_html()
        )
