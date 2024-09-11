# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class NaglowekListy(WLElement):
    NUMBERING = 'i'

    HTML_TAG = "h3"
    HTML_CLASS = "wl"

    EPUB_TAG = "div"
    EPUB_CLASS = "h3"
