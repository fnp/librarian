# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class Didaskalia(WLElement):
    SHOULD_HAVE_ID = True

    TXT_TOP_PARGIN = 2
    TXT_BOTTOM_MARGIN = 2
    TXT_LEGACY_TOP_MARGIN = 2
    TXT_LEGACY_BOTTOM_MARGIN = 0
    TXT_PREFIX = "/ "
    TXT_SUFFIX = " /"

    EPUB_TAG =_HTML_TAG = "div"
    EPUB_CLASS = HTML_CLASS = "didaskalia"
