# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class Nota(WLElement):
    CAN_HAVE_TEXT = False

    EPUB_TAG = HTML_TAG = "div"
    EPUB_CLASS = HTML_CLASS = "note"

    SUPPRESS_NUMBERING = {'main': 'i'}
