# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class Tabela(WLElement):
    NUMBERING = 'i'
    CAN_HAVE_TEXT = False

    TXT_TOP_MARGIN = 3
    TXT_BOTTOM_MARGIN = 3

    EPUB_TAG = HTML_TAG = 'table'

    def get_html_attr(self, builder):
        if self.attrib.get('ramka', '') == '1':
            return {
                'class': 'border'
            }
        return {}

    get_epub_attr = get_html_attr

                
