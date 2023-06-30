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
    EPUB_CLASS = HTML_CLASS = 'verse'

    @property
    def meta(self):
        if hasattr(self, 'stanza'):
            return self.stanza.meta
        return super(Wers, self).meta

    def _epub_build_inner(self, builder):
        super()._epub_build_inner(builder)
        builder.push_text('''\u00a0''')

