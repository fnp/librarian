# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class DlugiCytat(WLElement):
    CAN_HAVE_TEXT = False

    TXT_TOP_MARGIN = 3
    TXT_BOTTOM_MARGIN = 3

    HTML_TAG = 'blockquote'

    EPUB_TAG = 'div'
    EPUB_CLASS = 'block'

    FB2_TAG = 'cite'
