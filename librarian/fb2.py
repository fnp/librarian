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
functions.reg_person_name()


def sectionify(tree):
    """Finds section headers and adds a tree of _section tags."""
    sections = [
        'naglowek_czesc',
        'naglowek_akt', 'naglowek_rozdzial', 'naglowek_scena',
        'naglowek_podrozdzial']
    section_level = dict((v, k) for (k, v) in enumerate(sections))

    # We can assume there are just subelements an no text at section level.
    for level, section_name in reversed(list(enumerate(sections))):
        for header in tree.findall('//' + section_name):
            section = header.makeelement("_section")
            header.addprevious(section)
            section.append(header)
            sibling = section.getnext()
            while (sibling is not None and
                    section_level.get(sibling.tag, 1000) > level):
                section.append(sibling)
                sibling = section.getnext()


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

    document.clean_ed_note()
    document.clean_ed_note('abstrakt')

    style_filename = os.path.join(os.path.dirname(__file__), 'fb2/fb2.xslt')
    style = etree.parse(style_filename)

    replace_by_verse(document.edoc)
    sectionify(document.edoc)

    result = document.transform(style)

    return OutputFile.from_string(unicode(result).encode('utf-8'))

# vim:et
