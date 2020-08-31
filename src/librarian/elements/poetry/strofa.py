from copy import copy
from ..base import WLElement
from .wers import Wers


class Strofa(WLElement):
    TXT_TOP_MARGIN = 2
    TXT_BOTTOM_MARGIN = 2
    TXT_LEGACY_TOP_MARGIN = 1
    TXT_LEGACY_BOTTOM_MARGIN = 0

    def get_verses(self):
        from librarian.parser import parser

        verses = [
            parser.makeelement('wers')
        ]
        if self.text:
            # Before any tags. These are text-only verses.
            pieces = self.text.split('/')
            for piece in pieces[:-1]:
                verses[-1].text = piece
                verses.append(parser.makeelement('wers'))
            verses[-1].text = pieces[-1]

        for child in self:
            if child.tail:
                pieces = child.tail.split('/')
                child_copy = copy(child)
                child_copy.tail = pieces[0]
                verses[-1].append(child_copy)

                for piece in pieces[1:]:
                    verses.append(parser.makeelement('wers'))
                    verses[-1].text = piece
                
            else:
                verses[-1].append(child)

        for verse in verses:
            if len(verse) == 1 and isinstance(verse[0], Wers):
                assert not (verse.text or '').strip()
                assert not (verse[0].tail or '').strip()
                yield verse[0]
            else:
                yield verse

    def _build_inner(self, builder, build_method):
        for child in self.get_verses():
            getattr(child, build_method)(builder)
