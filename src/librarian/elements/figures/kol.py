# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class Kol(WLElement):
    EPUB_TAG = HTML_TAG = 'td'
    TXT_PREFIX = ' ' * 4
