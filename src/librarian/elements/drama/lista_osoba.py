# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class ListaOsoba(WLElement):
    TXT_TOP_MARGIN = 1
    TXT_BOTTOM_MARGIN = 1
    TXT_LEGACY_TOP_MARGIN = 1
    TXT_LEGACY_BOTTOM_MARGIN = 0
    TXT_PREFIX = " * "

    EPUB_TAG = HTML_TAG = "li"

    def html_build(self, builder):
        builder.enter_fragment('list')
        super(ListaOsoba, self).html_build(builder)
        builder.exit_fragment()
        
    def epub_build(self, builder):
        builder.enter_fragment('list')
        super(ListaOsoba, self).epub_build(builder)
        builder.exit_fragment()
