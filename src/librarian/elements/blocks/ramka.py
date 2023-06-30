# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class Ramka(WLElement):
    HTML_TAG = "div"
    HTML_CLASS = "ramka"

    EPUB_TAG = "div"
    EPUB_CLASS = "frame"
