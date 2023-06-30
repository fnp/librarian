# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class SlowoObce(WLElement):
    EPUB_TAG = HTML_TAG = 'em'
    EPUB_CLASS = HTML_CLASS = 'foreign-word'
