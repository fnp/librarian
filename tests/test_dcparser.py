#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from lxml import etree
from utils import get_file_path
from librarian import dcparser, html, ParseError
from utils import AutoTestMetaclass

class TestDCParser(unittest.TestCase):
    __metaclass__ = AutoTestMetaclass

    TEST_DIR = 'dcparser'

    def run_auto_test(self, in_data, out_data):
        info = dcparser.BookInfo.from_string(in_data).to_dict()
        should_be = eval(out_data)
        for key in should_be:
            self.assertEqual( info[key], should_be[key] )

class TestDCSerialize(unittest.TestCase):
    __metaclass__ = AutoTestMetaclass

    TEST_DIR = 'dcserialize'

    def run_auto_test(self, in_data, out_data):
        import lxml.etree
        # first parse the input
        info = dcparser.BookInfo.from_string(in_data)

        # serialize
        serialized = lxml.etree.tostring(info.to_etree(), encoding=unicode).encode('utf-8')

        # then parse again
        info_bis = dcparser.BookInfo.from_string(serialized)

        # check if they are the same
        for key in vars(info):
            self.assertEqual( getattr(info, key), getattr(info_bis, key))

        for key in vars(info_bis):
            self.assertEqual( getattr(info, key), getattr(info_bis, key))

class TestParserErrors(unittest.TestCase):
    def test_error(self):
        try:
            html.transform(get_file_path('erroneous', 'asnyk_miedzy_nami.xml'),
                           get_file_path('erroneous', 'asnyk_miedzy_nami.html'))
            self.fail()
        except ParseError:
            pass
            #self.assertEqual(e.position, (25, 13))    

if __name__ == '__main__':
    unittest.main()
