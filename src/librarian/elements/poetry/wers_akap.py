# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from .wers import Wers


class WersAkap(Wers):
    TXT_PREFIX = '  '

    HTML_CLASS = Wers.HTML_CLASS + ' verse-p'

    EPUB_ATTR = {
        "style": "margin-left: 1em"
    }
