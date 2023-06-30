# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class Dedykacja(WLElement):
    SHOULD_HAVE_ID = True

    TXT_LEGACY_TOP_MARGIN = 2

    EPUB_TAG = HTML_TAG = "div"
    EPUB_CLASS = HTML_CLASS = "dedication"
