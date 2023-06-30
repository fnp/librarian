# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import unittest
from librarian import dcparser
from lxml import etree
from os.path import splitext
from tests.utils import get_all_fixtures


class MetaTests(unittest.TestCase):
    def check_dcparser(self, xml_file, result_file):
        with open(xml_file, 'rb') as f:
            xml = f.read()
        with open(result_file) as f:
            result = f.read()
        info = dcparser.BookInfo.from_bytes(xml).to_dict()
        should_be = eval(result)
        for key in should_be:
            self.assertEqual(info[key], should_be[key])


    def test_dcparser(self):
        for fixture in get_all_fixtures('dcparser', '*.xml'):
            base_name = splitext(fixture)[0]
            with self.subTest(name=base_name):
                self.check_dcparser(fixture, base_name + '.out')

    def check_serialize(self, xml_file):
        with open(xml_file, 'rb') as f:
            xml = f.read()
        info = dcparser.BookInfo.from_bytes(xml)

        # serialize
        serialized = etree.tostring(info.to_etree(), encoding='unicode').encode('utf-8')
        # then parse again
        info_bis = dcparser.BookInfo.from_bytes(serialized)

        # check if they are the same
        for key in vars(info):
            self.assertEqual(getattr(info, key), getattr(info_bis, key))
        for key in vars(info_bis):
            self.assertEqual(getattr(info, key), getattr(info_bis, key))

    def test_serialize(self):
        for fixture in get_all_fixtures('dcparser', '*.xml'):
            with self.subTest(name=fixture):
                self.check_serialize(fixture)
