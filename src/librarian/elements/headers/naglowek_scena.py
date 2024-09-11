# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class NaglowekScena(WLElement):
    NUMBERING = 's'
    SECTION_PRECEDENCE = 2

    TXT_TOP_MARGIN = 4
    TXT_BOTTOM_MARGIN = 2
    TXT_LEGACY_TOP_MARGIN = 4
    TXT_LEGACY_BOTTOM_MARGIN = 0

    HTML_TAG = 'h3'

    EPUB_TAG = 'h2'
    EPUB_CLASS = 'h3'
    EPUB_START_CHUNK = False

