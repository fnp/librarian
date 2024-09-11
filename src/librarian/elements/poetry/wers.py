# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class Wers(WLElement):
    STRIP = True

    TXT_TOP_MARGIN = 1
    TXT_BOTTOM_MARGIN = 1
    TXT_LEGACY_TOP_MARGIN = 1
    TXT_LEGACY_BOTTOM_MARGIN = 0

    EPUB_TAG = HTML_TAG = 'div'
    EPUB_CLASS = 'verse'
    HTML_CLASS = 'wl verse'

    NUMBERING = 'main'

    @property
    def meta(self):
        if hasattr(self, 'stanza'):
            return self.stanza.meta
        return super(Wers, self).meta

    def _epub_build_inner(self, builder):
        super()._epub_build_inner(builder)
        builder.push_text('''\u00a0''')

    @property
    def has_visible_numbering(self):
        try:
            number = int(self.attrib['_visible_numbering'])
        except:
            return False
        return number == 1 or not(number % 5)

    @property
    def is_stretched(self):
        return self.find('.//tab[@szer="*"]') is not None

    def get_html_attr(self, builder):
        attr = super().get_html_attr(builder)
        if self.is_stretched:
            attr['class'] += ' verse-stretched'
        return attr

    def _html_build_inner(self, builder):
        if self.is_stretched:
            builder.start_element('span')
        super()._html_build_inner(builder)
        if self.is_stretched:
            builder.end_element()
