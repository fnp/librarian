# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class MottoPodpis(WLElement):
    NUMBERING = 'i'

    HTML_TAG = "p"
    HTML_CLASS = "wl motto_podpis"

    EPUB_TAG = "div"
    EPUB_CLASS = "motto_podpis"

    FB2_TAG = 'p'
