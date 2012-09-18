# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import os.path
from copy import deepcopy
from lxml import etree

from librarian import functions, OutputFile
from .epub import replace_by_verse


functions.reg_substitute_entities()

def transform(wldoc, verbose=False,
              cover=None, flags=None):
    """ produces a FB2 file

    cover: a cover.Cover object or True for default
    flags: less-advertising, working-copy
    """

    document = deepcopy(wldoc)
    del wldoc

    if flags:
        for flag in flags:
            document.edoc.getroot().set(flag, 'yes')

    style_filename = os.path.join(os.path.dirname(__file__), 'fb2/fb2.xslt')
    style = etree.parse(style_filename)

    replace_by_verse(document.edoc)

    result = document.transform(style)

    return OutputFile.from_string(unicode(result).encode('utf-8'))

# vim:et
