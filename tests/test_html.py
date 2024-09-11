# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import io
from unittest import TestCase
from librarian.builders import builders
from librarian.document import WLDocument
from .utils import get_fixture


class TransformTest(TestCase):
    maxDiff = None

    def test_transform(self):
        expected_output_file_path = get_fixture('text', 'asnyk_miedzy_nami_expected.html')
        html = WLDocument(
            filename=get_fixture('text', 'miedzy-nami-nic-nie-bylo.xml')
        ).build(builders['html']).get_bytes().decode('utf-8')

        with open(expected_output_file_path) as f:
            self.assertEqual(html, f.read())

    def test_empty(self):
        self.assertIsNone(
            WLDocument(
                filename=io.BytesIO(b'<utwor />'),
            ).build(builders['html'], base_url='/')
        )
