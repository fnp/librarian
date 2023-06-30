# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import re
from tempfile import NamedTemporaryFile
import unittest
from librarian import DirDocProvider
from librarian.parser import WLDocument
from .utils import get_fixture


class PdfTests(unittest.TestCase):
    def test_transform(self):
        temp = NamedTemporaryFile(delete=False)
        temp.close()
        WLDocument.from_file(
            get_fixture('text', 'asnyk_zbior.xml'),
            provider=DirDocProvider(get_fixture('text', ''))
        ).as_pdf(save_tex=temp.name)
        with open(temp.name, 'rb') as f:
            tex = f.read().decode('utf-8')

        # Check contributor list.
        editors = re.search(r'\\def\\editors\{Opracowanie redakcyjne i przypisy: ([^}]*?)\.\s*\}', tex)
        self.assertEqual(editors.group(1), "Adam Fikcyjny, Aleksandra Sekuła, Olga Sutkowska")
