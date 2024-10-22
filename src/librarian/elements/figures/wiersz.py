# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class Wiersz(WLElement):
    CAN_HAVE_TEXT = False
    EPUB_TAG = HTML_TAG = FB2_TAG = 'tr'
    TXT_TOP_MARGIN = 1
    TXT_BOTTOM_MARGIN = 1
