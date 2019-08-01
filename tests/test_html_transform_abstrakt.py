# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from __future__ import unicode_literals

from librarian.parser import WLDocument
from librarian.html import transform_abstrakt
from nose.tools import *
from .utils import get_fixture


def test_fragments():
    transform_abstrakt(
        WLDocument.from_file(
            get_fixture('text', 'abstrakt.xml'),
            parse_dublincore=False
        ).edoc.getroot().find('.//abstrakt')
    )
