# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class SekcjaAsterysk(WLElement):
    TXT_TOP_MARGIN = 2
    TXT_BOTTOM_MARGIN = 4

    EPUB_TAG = HTML_TAG = "p"
    HTML_CLASS = HTML_CLASS = "spacer-asterisk"

    def txt_build_inner(self, builder):
        builder.push_text('*')

    def html_build_inner(self, builder):
        builder.push_text("*")

    epub_build_inner = html_build_inner

