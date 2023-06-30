# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class Akap(WLElement):
    STRIP = True
    SHOULD_HAVE_ID = True

    TXT_TOP_MARGIN = 2
    TXT_BOTTOM_MARGIN = 2
    TXT_LEGACY_TOP_MARGIN = 2
    TXT_LEGACY_BOTTOM_MARGIN = 0

    HTML_TAG = 'p'
    EPUB_CLASS = HTML_CLASS = 'paragraph'

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
 
