# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class Akap(WLElement):
    STRIP = True
    NUMBERING = 'main'

    TXT_TOP_MARGIN = 2
    TXT_BOTTOM_MARGIN = 2

    EPUB_CLASS = 'paragraph'

    HTML_TAG = 'p'
    HTML_CLASS = 'wl paragraph'

    has_visible_numbering = True

    @property
    def EPUB_TAG(self):
        try:
            return self._set_EPUB_TAG
        except AttributeError:
            if self.in_context_of('START_INLINE'):
                self.signal('INLINE')
                self._set_EPUB_TAG = None
            else:
                self._set_EPUB_TAG = 'p'
            return self._set_EPUB_TAG
 
