# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class NaglowekPodrozdzial(WLElement):
    NUMBERING = 's'
    SECTION_PRECEDENCE = 3

    TXT_TOP_MARGIN = 3
    TXT_BOTTOM_MARGIN = 2

    HTML_TAG = "h4"

    EPUB_TAG = "h2"
    EPUB_CLASS = "h4"
