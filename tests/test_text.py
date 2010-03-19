#!/usr/bin/env python
# encoding: utf-8

import unittest

from utils import get_file_path
from librarian import dcparser
from librarian import text, NoDublinCore


class TestXML(unittest.TestCase):
    def test_no_dublincore(self):
        try:
            text.transform(get_file_path('text', 'asnyk_miedzy_nami.xml'),
                           get_file_path('text', 'asnyk_miedzy_nami.txt'))
            self.fail()
        except NoDublinCore, e:
            pass


if __name__ == '__main__':
    unittest.main()
