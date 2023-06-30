# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class NaglowekListy(WLElement):
    SHOULD_HAVE_ID = True

    HTML_TAG = "h3"

    EPUB_TAG = "div"
    EPUB_CLASS = "h3"
