# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from copy import copy
import re
from ..base import WLElement
from .wers import Wers


class Strofa(WLElement):
    NUMBERING = 'i'

    TXT_TOP_MARGIN = 2
    TXT_BOTTOM_MARGIN = 2
    TXT_LEGACY_TOP_MARGIN = 1
    TXT_LEGACY_BOTTOM_MARGIN = 0

    EPUB_TAG = HTML_TAG = 'div'
    EPUB_CLASS = HTML_CLASS = 'stanza'

    def epub_build(self, builder):
        super().epub_build(builder)
        builder.start_element(
            'div',
            {
                'class': 'stanza-spacer'
            }
        )
        builder.push_text('\u00a0');
        builder.end_element()

    def preprocess(self):
        from librarian.parser import parser

        verses = [
            parser.makeelement('wers')
        ]
        if self.text:
            # Before any tags. These are text-only verses.
            pieces = re.split(r"/\s+", self.text)
            for piece in pieces[:-1]:
                verses[-1].text = piece
                verses.append(parser.makeelement('wers'))
            verses[-1].text = pieces[-1]

        for child in self:
            if child.tail:
                pieces = re.split(r"/\s+", child.tail)
                child_copy = copy(child)
                child_copy.tail = pieces[0]
                verses[-1].append(child_copy)

                for piece in pieces[1:]:
                    verses.append(parser.makeelement('wers'))
                    verses[-1].text = piece
                
            else:
                verses[-1].append(child)

        verses = [
            verse[0] if len(verse) == 1 and isinstance(verse[0], Wers)
            else verse
            for verse in verses
        ]

        while len(self):
            self.remove(self[0])
        self.text = None

        for verse in verses:
            self.append(verse)
