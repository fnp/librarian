# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from tempfile import NamedTemporaryFile
from nose.tools import *
from librarian import DirDocProvider
from librarian.parser import WLDocument
from utils import get_fixture


def test_transform():
    temp = NamedTemporaryFile(delete=False)
    temp.close()
    WLDocument.from_file(
            get_fixture('text', 'asnyk_zbior.xml'),
            provider=DirDocProvider(get_fixture('text', ''))
        ).as_pdf(save_tex=temp.name)
    tex = open(temp.name).read().decode('utf-8')
    print tex

    # Check contributor list.
    editors = re.search(ur'\\def\\editors\{Opracowanie redakcyjne i przypisy: ([^}]*?)\.\s*\}', tex)
    assert_equal(editors.group(1), u"Adam Fikcyjny, Aleksandra Sekuła, Olga Sutkowska")
