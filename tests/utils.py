# -*- coding: utf-8 -*-
#
# Copyright © 2008,2009,2010 Fundacja Nowoczesna Polska  
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# For full license text see COPYING or <http://www.gnu.org/licenses/agpl.html>
#
from __future__ import with_statement
from os.path import realpath, join, dirname
import glob
import os

def get_fixture_dir(dir_name):
    """Returns path to fixtures directory dir_name."""
    return realpath(join(dirname(__file__), 'files', dir_name))


def get_fixture(dir_name, file_name):
    """Returns path to fixture file_name in directory dir_name."""
    return join(get_fixture_dir(dir_name), file_name)


def get_all_fixtures(dir_name, glob_pattern='*'):
    """Returns list of paths for fixtures in directory dir_name matching the glob_pattern."""
    return [get_fixture(dir_name, file_name) for file_name in glob.glob(join(get_fixture_dir(dir_name), glob_pattern))]


def remove_output_file(dir_name, file_name):
    try:
        os.remove(get_fixture(dir_name, file_name))
    except:
        pass
