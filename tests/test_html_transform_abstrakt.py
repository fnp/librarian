# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import unittest
from librarian.parser import WLDocument
from librarian.html import transform_abstrakt
from .utils import get_fixture


class AbstractTests(unittest.TestCase):
    def test_abstrakt(self):
        transform_abstrakt(
            WLDocument.from_file(
                get_fixture('text', 'abstrakt.xml'),
                parse_dublincore=False
            ).edoc.getroot().find('.//abstrakt')
        )
