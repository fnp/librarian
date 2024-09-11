# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from .base import HeaderElement


class DzieloNadrzedne(HeaderElement):
    TXT_BOTTOM_MARGIN = 1
    TXT_LEGACY_BOTTOM_MARGIN = 1

    HTML_CLASS = "wl collection"

    def epub_build(self, builder):
        return
