# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from librarian import dcparser
from lxml import etree
from nose.tools import *
from os.path import splitext
from tests.utils import get_all_fixtures
import codecs
from datetime import date


def check_dcparser(xml_file, result_file):
    xml = file(xml_file).read()
    result = codecs.open(result_file, encoding='utf-8').read()
    info = dcparser.BookInfo.from_string(xml).to_dict()
    should_be = eval(result)
    for key in should_be:
        assert_equals(info[key], should_be[key])


def test_dcparser():
    for fixture in get_all_fixtures('dcparser', '*.xml'):
        base_name = splitext(fixture)[0]
        yield check_dcparser, fixture, base_name + '.out'


def check_serialize(xml_file):
    xml = file(xml_file).read()
    info = dcparser.BookInfo.from_string(xml)

    # serialize
    serialized = etree.tostring(info.to_etree(), encoding=unicode).encode('utf-8')
    # then parse again
    info_bis = dcparser.BookInfo.from_string(serialized)

    # check if they are the same
    for key in vars(info):
        assert_equals(getattr(info, key), getattr(info_bis, key))
    for key in vars(info_bis):
        assert_equals(getattr(info, key), getattr(info_bis, key))


def test_serialize():
    for fixture in get_all_fixtures('dcparser', '*.xml'):
        yield check_serialize, fixture


def test_asdate():
    assert_equals(dcparser.as_date(u"2010-10-03"), date(2010, 10, 03))
    assert_equals(dcparser.as_date(u"2011"), date(2011, 1, 1))
    assert_equals(dcparser.as_date(u"2 poł. XIX w."), date(1950, 1, 1))
    assert_equals(dcparser.as_date(u"XVII w., l. 20"), date(1720, 1, 1))
    assert_equals(dcparser.as_date(u"po 1460"), date(1460, 1, 1))
    assert_equals(dcparser.as_date(u"ok. 1813-1814"), date(1813, 1, 1))
    assert_equals(dcparser.as_date(u"ok.1876-ok.1886"), date(1876, 1, 1))
    assert_equals(dcparser.as_date(u"1893/1894"), date(1893, 1, 1))
