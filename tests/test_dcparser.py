# -*- coding: utf-8 -*-
#
#    This file is part of Librarian.
#
#    Copyright © 2008,2009,2010 Fundacja Nowoczesna Polska <fundacja@nowoczesnapolska.org.pl>
#    
#    For full list of contributors see AUTHORS file. 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from librarian import dcparser
from lxml import etree
from nose.tools import *
from os.path import splitext
from tests.utils import get_all_fixtures
import codecs


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

