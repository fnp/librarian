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
from librarian import text, NoDublinCore
from nose.tools import *
from utils import get_fixture, remove_output_file


def teardown_transform():
    remove_output_file('text', 'asnyk_miedzy_nami.txt')


@with_setup(None, teardown_transform)
def test_transform():
    output_file_path = get_fixture('text', 'asnyk_miedzy_nami.txt')
    expected_output_file_path = get_fixture('text', 'asnyk_miedzy_nami_expected.txt')
    
    text.transform(
        get_fixture('text', 'asnyk_miedzy_nami.xml'),
        output_file_path,
    )
    
    assert_equal(file(output_file_path).read(), file(expected_output_file_path).read())


@with_setup(None, teardown_transform)
@raises(NoDublinCore)
def test_no_dublincore():
    text.transform(
        get_fixture('text', 'asnyk_miedzy_nami_nodc.xml'),
        get_fixture('text', 'asnyk_miedzy_nami_nodc.txt'),
    )


@with_setup(None, teardown_transform)
def test_passing_parse_dublincore_to_transform():
    """Passing parse_dublincore=False to transform omits DublinCore parsing."""
    text.transform(
        get_fixture('text', 'asnyk_miedzy_nami_nodc.xml'),
        get_fixture('text', 'asnyk_miedzy_nami.txt'),
        parse_dublincore=False,
    )
    