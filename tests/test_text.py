# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import unittest
from librarian.builders import builders
from librarian.document import WLDocument
from .utils import get_fixture


class TextTests(unittest.TestCase):
    maxDiff = None

    def test_transform(self):
        expected_output_file_path = get_fixture('text', 'asnyk_miedzy_nami_expected.txt')

        text = WLDocument(
            filename=get_fixture('text', 'miedzy-nami-nic-nie-bylo.xml')
        ).build(builders['txt']).get_bytes().decode('utf-8')

        with open(expected_output_file_path, 'rb') as f:
            self.assertEqual(text, f.read().decode('utf-8'))

    
    def test_transform_raw(self):
        expected_output_file_path = get_fixture('text', 'asnyk_miedzy_nami_expected_raw.txt')

        text = WLDocument(
            filename=get_fixture('text', 'miedzy-nami-nic-nie-bylo.xml')
        ).build(builders['txt'], raw_text=True).get_bytes().decode('utf-8')

        with open(expected_output_file_path, 'rb') as f:
            self.assertEqual(text, f.read().decode('utf-8'))
