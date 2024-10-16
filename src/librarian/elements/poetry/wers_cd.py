# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from .wers import Wers

class WersCd(Wers):
    HTML_CLASS = Wers.HTML_CLASS + ' verse-cont'

    def txt_build_inner(self, builder):
        builder.push_text(' ' * 24, prepared=True)
        super().txt_build_inner(builder)

    EPUB_ATTR = {
        "style": "margin-left: 12em",
    }
