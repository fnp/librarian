# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class ListaOsoba(WLElement):
    NUMBERING = "i"

    TXT_TOP_MARGIN = 1
    TXT_BOTTOM_MARGIN = 1
    TXT_PREFIX = " * "

    EPUB_TAG = HTML_TAG = "li"
    HTML_CLASS = "wl"

    def html_build(self, builder):
        builder.enter_fragment('list')
        super(ListaOsoba, self).html_build(builder)
        builder.exit_fragment()
        
    def epub_build(self, builder):
        builder.enter_fragment('list')
        super(ListaOsoba, self).epub_build(builder)
        builder.exit_fragment()
