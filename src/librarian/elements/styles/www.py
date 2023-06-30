# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class WWW(WLElement):
    EPUB_TAG = 'a'

    def get_epub_attr(self, builder):
        attr = super().get_epub_attr(builder)
        attr['href'] = self.text
        return attr

