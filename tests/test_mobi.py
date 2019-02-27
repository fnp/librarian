# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from __future__ import unicode_literals

from zipfile import ZipFile
from lxml import html
from nose.tools import *
from librarian import DirDocProvider
from librarian.parser import WLDocument
from tests.utils import get_fixture


def test_transform():
    mobi = WLDocument.from_file(
            get_fixture('text', 'asnyk_zbior.xml'),
            provider=DirDocProvider(get_fixture('text', ''))
        ).as_mobi(converter_path='true').get_file()
