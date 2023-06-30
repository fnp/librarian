# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class MottoPodpis(WLElement):
    SHOULD_HAVE_ID = True
    HTML_TAG = "p"
    EPUB_CLASS = HTML_CLASS = "motto_podpis"

    EPUB_TAG = "div"
    
