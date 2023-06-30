# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import unittest
from librarian import NoDublinCore
from librarian.builders import builders
from librarian.parser import WLDocument as LegacyWLDocument
from librarian.document import WLDocument
from .utils import get_fixture


class TextTests(unittest.TestCase):
    maxDiff = None

    def test_transform_legacy(self):
        expected_output_file_path = get_fixture('text', 'asnyk_miedzy_nami_expected.txt')

        text = LegacyWLDocument.from_file(
            get_fixture('text', 'miedzy-nami-nic-nie-bylo.xml')
        ).as_text().get_bytes().decode('utf-8')

        with open(expected_output_file_path, 'rb') as f:
            self.assertEqual(text, f.read().decode('utf-8'))

    def test_transform(self):
        expected_output_file_path = get_fixture('text', 'asnyk_miedzy_nami_expected.txt')

        text = WLDocument(
            filename=get_fixture('text', 'miedzy-nami-nic-nie-bylo.xml')
        ).build(builders['txt']).get_bytes().decode('utf-8')

        with open(expected_output_file_path, 'rb') as f:
            self.assertEqual(text, f.read().decode('utf-8'))

    
    def test_transform_raw(self):
        expected_output_file_path = get_fixture('text', 'asnyk_miedzy_nami_expected_raw.txt')

        text = LegacyWLDocument.from_file(
            get_fixture('text', 'miedzy-nami-nic-nie-bylo.xml')
        ).as_text(flags=['raw-text']).get_bytes().decode('utf-8')

        with open(expected_output_file_path, 'rb') as f:
            self.assertEqual(text, f.read().decode('utf-8'))

    def test_no_dublincore(self):
        with self.assertRaises(NoDublinCore):
            LegacyWLDocument.from_file(
                get_fixture('text', 'asnyk_miedzy_nami_nodc.xml')
            ).as_text()

    def test_passing_parse_dublincore_to_transform(self):
        """Passing parse_dublincore=False to the constructor omits DublinCore parsing."""
        LegacyWLDocument.from_file(
            get_fixture('text', 'asnyk_miedzy_nami_nodc.xml'),
            parse_dublincore=False,
        ).as_text()
