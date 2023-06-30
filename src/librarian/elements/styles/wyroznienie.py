# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class Wyroznienie(WLElement):
    TXT_PREFIX = "*"
    TXT_SUFFIX = "*"

    EPUB_TAG = HTML_TAG = "em"
    EPUB_CLASS = HTML_CLASS = "author-emphasis"
