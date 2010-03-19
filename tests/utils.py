# -*- coding: utf-8 -*-
#
#    This file is part of Librarian.
#
#    Copyright © 2008,2009,2010 Fundacja Nowoczesna Polska <fundacja@nowoczesnapolska.org.pl>
#    
#    For full list of contributors see AUTHORS file. 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
