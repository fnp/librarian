# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class Didaskalia(WLElement):
    NUMBERING = 'i'

    TXT_TOP_PARGIN = 2
    TXT_BOTTOM_MARGIN = 2
    TXT_PREFIX = "/ "
    TXT_SUFFIX = " /"

    EPUB_TAG = HTML_TAG = "div"
    EPUB_CLASS = HTML_CLASS = "didaskalia"
