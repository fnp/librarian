# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
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
        open(get_fixture('text', 'asnyk_miedzy_nami.xml')),
        open(output_file_path, 'w'),
    )

    assert_equal(file(output_file_path).read(), file(expected_output_file_path).read())


@with_setup(None, teardown_transform)
@raises(NoDublinCore)
def test_no_dublincore():
    text.transform(
        open(get_fixture('text', 'asnyk_miedzy_nami_nodc.xml')),
        open(get_fixture('text', 'asnyk_miedzy_nami.txt'), 'w'),
    )


@with_setup(None, teardown_transform)
def test_passing_parse_dublincore_to_transform():
    """Passing parse_dublincore=False to transform omits DublinCore parsing."""
    text.transform(
        open(get_fixture('text', 'asnyk_miedzy_nami_nodc.xml')),
        open(get_fixture('text', 'asnyk_miedzy_nami.txt'), 'w'),
        parse_dublincore=False,
    )
