# -*- coding: utf-8 -*-
from librarian import html, NoDublinCore
from nose.tools import *
from utils import get_fixture, remove_output_file


def teardown_transform():
    remove_output_file('text', 'asnyk_miedzy_nami.html')


@with_setup(None, teardown_transform)
def test_transform():
    output_file_path = get_fixture('text', 'asnyk_miedzy_nami.html')
    expected_output_file_path = get_fixture('text', 'asnyk_miedzy_nami_expected.html')
    
    html.transform(
        get_fixture('text', 'asnyk_miedzy_nami.xml'),
        output_file_path,
    )
    
    assert_equal(file(output_file_path).read(), file(expected_output_file_path).read())


@with_setup(None, teardown_transform)
@raises(NoDublinCore)
def test_no_dublincore():
    html.transform(
        get_fixture('text', 'asnyk_miedzy_nami_nodc.xml'),
        get_fixture('text', 'asnyk_miedzy_nami_nodc.html'),
    )


@with_setup(None, teardown_transform)
def test_passing_parse_dublincore_to_transform():
    """Passing parse_dublincore=False to transform omits DublinCore parsing."""
    html.transform(
        get_fixture('text', 'asnyk_miedzy_nami_nodc.xml'),
        get_fixture('text', 'asnyk_miedzy_nami.html'),
        parse_dublincore=False,
    )
