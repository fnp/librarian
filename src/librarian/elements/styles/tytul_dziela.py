# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class TytulDziela(WLElement):
    EPUB_TAG = HTML_TAG = 'em'
    EPUB_CLASS = HTML_CLASS = 'book-title'

    def normalize_text(self, text, builder):
        txt = super(TytulDziela, self).normalize_text(text, builder)
        if self.attrib.get('typ') == '1':
            txt = '„{txt}”'.format(txt=txt)
        return txt
