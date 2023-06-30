# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class IndeksDolny(WLElement):
    TXT_PREFIX = "_"

    EPUB_TAG = HTML_TAG = "sub"
