# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from lxml import etree
from librarian import SSTNS
from .meta import Metadata


class TextElement(etree.ElementBase):
    @property
    def meta(self):
        m = self.find(SSTNS('metadata'))
        if m is None:
            return Metadata.about(self)
        return m


class Span(TextElement):
    pass


class Div(TextElement):
    pass


class Section(TextElement):
    pass


class Header(TextElement):
    pass


class Aside(TextElement):
    pass
