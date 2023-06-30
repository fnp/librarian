# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from .wers import Wers

class WersCd(Wers):
    def _txt_build_inner(self, builder):
        builder.push_text(' ' * 24, prepared=True)
        super(WersCd, self)._txt_build_inner(builder)

    HTML_ATTR = {
        "style": "padding-left: 12em",
    }

    EPUB_ATTR = {
        "style": "margin-left: 12em",
    }
