# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class NaglowekCzesc(WLElement):
    NUMBERING = 's'
    SECTION_PRECEDENCE = 1
    
    TXT_TOP_MARGIN = 5
    TXT_BOTTOM_MARGIN = 2

    EPUB_TAG = HTML_TAG = "h2"
    HTML_CLASS = "wl"

    EPUB_CLASS = "h2"
    EPUB_START_CHUNK = True
