# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class NaglowekOsoba(WLElement):
    NUMBERING = 'i'

    TXT_TOP_MARGIN = 3
    TXT_BOTTOM_MARGIN = 2
    TXT_LEGACY_TOP_MARGIN = 3
    TXT_LEGACY_BOTTOM_MARGIN = 0

    HTML_TAG = "h4"

    EPUB_TAG = "h2"
    EPUB_CLASS = "h4"
