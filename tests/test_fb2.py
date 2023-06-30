# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from unittest import TestCase
from librarian import NoDublinCore
from librarian.parser import WLDocument
from .utils import get_fixture


class FB2Tests(TestCase):
    maxDiff = None

    def test_transform(self):
        expected_output_file_path = get_fixture('text', 'asnyk_miedzy_nami_expected.fb2')

        text = WLDocument.from_file(
            get_fixture('text', 'miedzy-nami-nic-nie-bylo.xml')
        ).as_fb2().get_bytes().decode('utf-8')

        with open(expected_output_file_path, 'rb') as f:
            self.assertEqual(text, f.read().decode('utf-8'))

