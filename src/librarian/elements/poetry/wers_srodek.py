# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from .wers import Wers


class WersSrodek(Wers):
    TXT_PREFIX = '           '

    HTML_CLASS = Wers.HTML_CLASS + ' verse-center'

    EPUB_ATTR = {
        "style": "text-align: center",
    }
