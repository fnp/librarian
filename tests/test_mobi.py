# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import unittest
from zipfile import ZipFile
from lxml import html
from librarian import DirDocProvider
from librarian.builders import MobiBuilder
from librarian.document import WLDocument
from tests.utils import get_fixture


class MobiTests(unittest.TestCase):
    def test_transform(self):
        mobi = MobiBuilder().build(
            WLDocument(
                get_fixture('text', 'asnyk_zbior.xml'),
                provider=DirDocProvider(get_fixture('text', ''))
            )
        )
