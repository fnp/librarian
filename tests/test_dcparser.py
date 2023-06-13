# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from __future__ import unicode_literals

from librarian import dcparser
from lxml import etree
from nose.tools import *
from os.path import splitext
from tests.utils import get_all_fixtures
import codecs
from datetime import date


def check_dcparser(xml_file, result_file):
    xml = open(xml_file, 'rb').read()
    result = codecs.open(result_file, encoding='utf-8').read()
    info = dcparser.BookInfo.from_bytes(xml).to_dict()
    should_be = eval(result)
    for key in should_be:
        assert_equals(info[key], should_be[key])


def test_dcparser():
    for fixture in get_all_fixtures('dcparser', '*.xml'):
        base_name = splitext(fixture)[0]
        yield check_dcparser, fixture, base_name + '.out'


def check_serialize(xml_file):
    xml = open(xml_file, 'rb').read()
    info = dcparser.BookInfo.from_bytes(xml)

    # serialize
    serialized = etree.tostring(info.to_etree(), encoding='unicode').encode('utf-8')
    # then parse again
    info_bis = dcparser.BookInfo.from_bytes(serialized)

    # check if they are the same
    for key in vars(info):
        assert_equals(getattr(info, key), getattr(info_bis, key))
    for key in vars(info_bis):
        assert_equals(getattr(info, key), getattr(info_bis, key))


def test_serialize():
    for fixture in get_all_fixtures('dcparser', '*.xml'):
        yield check_serialize, fixture
