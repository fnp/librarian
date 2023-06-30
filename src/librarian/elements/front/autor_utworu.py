# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from .base import HeaderElement


class AutorUtworu(HeaderElement):
    TXT_BOTTOM_MARGIN = 2
    TXT_LEGACY_BOTTOM_MARGIN = 2

    HTML_CLASS = 'author'

    def epub_build(self, builder):
        return
