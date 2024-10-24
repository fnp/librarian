# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class SeparatorLinia(WLElement):
    TXT_TOP_MARGIN = 4
    TXT_BOTTOM_MARGIN = 4

    EPUB_TAG = HTML_TAG = "hr"
    EPUB_CLASS = HTML_CLASS = "spacer-line"
    
    def txt_build_inner(self, builder):
        builder.push_text('-' * 48)

    def fb2_build(self, builder):
        builder.simple_element('empty-line')
        builder.simple_element('p', '—' * 8)
        builder.simple_element('empty-line')

