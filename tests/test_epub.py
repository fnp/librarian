# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import subprocess
import unittest
from zipfile import ZipFile
from ebooklib import epub
from lxml import html
from librarian import DirDocProvider
from librarian.builders import EpubBuilder
from librarian.document import WLDocument
from tests.utils import get_fixture


class EpubTests(unittest.TestCase):
    def test_transform(self):
        epub_file = EpubBuilder().build(
            WLDocument(
                get_fixture('text', 'asnyk_zbior.xml'),
                provider=DirDocProvider(get_fixture('text', ''))
            )
        )
        zipf = ZipFile(epub_file.get_file())

        # Check contributor list.
        last = zipf.open('EPUB/last.xhtml')
        tree = html.parse(last)
        editors_attribution = False
        for par in tree.findall("//p"):
            if par.text.startswith('Opracowanie redakcyjne i przypisy:'):
                editors_attribution = True
                self.assertEqual(
                    par.text.rstrip(),
                    'Opracowanie redakcyjne i przypisy: '
                    'Adam Fikcyjny, Aleksandra Sekuła, Olga Sutkowska.')
        self.assertTrue(editors_attribution)

        # Check that we have a valid EPUB.
        self.assertEqual(
            subprocess.call([
                'epubcheck', '-quiet', epub_file.get_filename()
            ]),
            0
        )

        book = epub.read_epub(epub_file.get_filename())

        # Check that guide items are there.
        self.assertEqual(
            book.guide,
            [
                {'href': 'cover.xhtml', 'title': 'Okładka', 'type': 'cover'},
                {'href': 'part1.xhtml', 'title': 'Początek', 'type': 'text'},
            ]
        )

        # Check that metadata is there.
        DC = "http://purl.org/dc/elements/1.1/"
        OPF = "http://www.idpf.org/2007/opf"

        self.assertEqual(
            book.get_metadata(OPF, "cover"),
            [(None, {'name': 'cover', 'content': 'cover-img'})]
        )
        self.assertEqual(
            book.get_metadata(DC, "title"),
            [('Poezye', {})]
        )
        self.assertEqual(
            book.get_metadata(DC, "language"),
            [('pl', {})]
        )
        self.assertEqual(
            book.get_metadata(DC, "identifier"),
            [('http://wolnelektury.pl/katalog/lektura/poezye', {
                'id': 'id',
            })]
        )
        self.assertEqual(
            book.get_metadata(DC, "creator"),
            [('Adam Asnyk', {"id": "creator0"})]
        )
        self.assertEqual(
            book.get_metadata(DC, "publisher"),
            [('Fundacja Wolne Lektury', {})]
        )
        self.assertEqual(
            book.get_metadata(DC, "date"),
            [("2007-09-06", {})]
        )
