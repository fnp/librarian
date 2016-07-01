# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import os
from tempfile import NamedTemporaryFile
from nose.tools import *
from librarian import IOFile


def test_iofile_from_string_reusable():
    some_file = IOFile.from_string("test")
    some_file.get_file().read()
    assert_equal(some_file.get_file().read(), "test")


def test_iofile_from_filename_reusable():
    temp = NamedTemporaryFile(delete=False)
    try:
        temp.write('test')
        temp.close()
        some_file = IOFile.from_filename(temp.name)
        some_file.get_file().read()
        assert_equal(some_file.get_file().read(), "test")
    finally:
        os.unlink(temp.name)
