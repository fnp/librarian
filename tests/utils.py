# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from __future__ import with_statement
from os.path import realpath, join, dirname
import glob


def get_fixture_dir(dir_name):
    """Returns path to fixtures directory dir_name."""
    return realpath(join(dirname(__file__), 'files', dir_name))


def get_fixture(dir_name, file_name):
    """Returns path to fixture file_name in directory dir_name."""
    return join(get_fixture_dir(dir_name), file_name)


def get_all_fixtures(dir_name, glob_pattern='*'):
    """Returns list of paths for fixtures in directory dir_name matching the glob_pattern."""
    return [get_fixture(dir_name, file_name) for file_name in glob.glob(join(get_fixture_dir(dir_name), glob_pattern))]
