# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class SekcjaSwiatlo(WLElement):
    TXT_BOTTOM_MARGIN = 6

    HTML_TAG = "hr"
    HTML_CLASS = "spacer"

    EPUB_TAG = 'p'
    EPUB_CLASS = 'spacer'

    def epub_build_inner(self, builder):
        builder.push_text("\u00a0")

    def fb2_build(self, builder):
        for i in range(3):
            builder.simple_element('empty-line')
