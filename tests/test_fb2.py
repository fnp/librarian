# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from __future__ import unicode_literals

from librarian import NoDublinCore
from librarian.parser import WLDocument
from nose.tools import *
from .utils import get_fixture


def test_transform():
    expected_output_file_path = get_fixture('text', 'asnyk_miedzy_nami_expected.fb2')

    text = WLDocument.from_file(
            get_fixture('text', 'miedzy-nami-nic-nie-bylo.xml')
        ).as_fb2().get_bytes()

    assert_equal(text, open(expected_output_file_path, 'rb').read())

