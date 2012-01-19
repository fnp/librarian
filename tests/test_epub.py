# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from librarian import DirDocProvider
from librarian.parser import WLDocument
from nose.tools import *
from utils import get_fixture


def test_transform():
    WLDocument.from_file(
            get_fixture('text', 'asnyk_zbior.xml'),
            provider=DirDocProvider(get_fixture('text', ''))
        ).as_epub(flags=['without_fonts'])
