# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class Motto(WLElement):
    NUMBERING = 'i'

    TXT_LEGACY_TOP_MARGIN = 4
    TXT_LEGACY_BOTTOM_MARGIN = 2

    EPUB_TAG = HTML_TAG = "div"
    EPUB_CLASS = HTML_CLASS = "motto"
