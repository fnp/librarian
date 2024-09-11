# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import unittest
from librarian.document import WLDocument
from librarian.builders.html import AbstraktHtmlBuilder
from .utils import get_fixture


class AbstractTests(unittest.TestCase):
    def test_abstrakt(self):
        builder = AbstraktHtmlBuilder()
        got = builder.build(
            WLDocument(
                filename=get_fixture('text', 'abstrakt.xml'),
            )
        ).get_bytes().decode('utf-8')
        with open(get_fixture('text', 'abstrakt.expected.html')) as f:
            expected = f.read()
        self.assertEqual(expected, got)
