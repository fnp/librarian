# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import re
from copy import deepcopy
from lxml import etree

from librarian import WLNS


class Stanza:
    """
    Converts / verse endings into verse elements in a stanza.

    Slashes may only occur directly in the stanza. Any slashes in subelements
    will be ignored, and the subelements will be put inside verse elements.

    >>> s = etree.fromstring(
    ...         "<strofa>a <b>c</b> <b>c</b>/\\nb<x>x/\\ny</x>c/ \\nd</strofa>"
    ...     )
    >>> Stanza(s).versify()
    >>> print(etree.tostring(s, encoding='unicode', pretty_print=True).strip())
    <strofa>
      <wers_normalny>a <b>c</b><b>c</b></wers_normalny>
      <wers_normalny>b<x>x/
    y</x>c</wers_normalny>
      <wers_normalny>d</wers_normalny>
    </strofa>

    """
    def __init__(self, stanza_elem):
        self.stanza = stanza_elem
        self.verses = []
        self.open_verse = None

    def versify(self):
        self.push_text(self.stanza.text)
        for elem in self.stanza:
            self.push_elem(elem)
            self.push_text(elem.tail)
        tail = self.stanza.tail
        self.stanza.clear()
        self.stanza.tail = tail
        self.stanza.extend(
            verse for verse in self.verses
            if verse.text or len(verse) > 0
        )

    def open_normal_verse(self):
        self.open_verse = self.stanza.makeelement("wers_normalny")
        self.verses.append(self.open_verse)

    def get_open_verse(self):
        if self.open_verse is None:
            self.open_normal_verse()
        return self.open_verse

    def push_text(self, text):
        if not text:
            return
        for i, verse_text in enumerate(re.split(r"/\s*\n", text)):
            if i:
                self.open_normal_verse()
            if not verse_text.strip():
                continue
            verse = self.get_open_verse()
            if len(verse):
                verse[-1].tail = (verse[-1].tail or "") + verse_text
            else:
                verse.text = (verse.text or "") + verse_text

    def push_elem(self, elem):
        if elem.tag.startswith("wers"):
            verse = deepcopy(elem)
            verse.tail = None
            self.verses.append(verse)
            self.open_verse = verse
        else:
            appended = deepcopy(elem)
            appended.tail = None
            self.get_open_verse().append(appended)


def replace_by_verse(tree):
    """ Find stanzas and create new verses in place of a '/' character """

    stanzas = tree.findall('.//' + WLNS('strofa'))
    for stanza in stanzas:
        Stanza(stanza).versify()
