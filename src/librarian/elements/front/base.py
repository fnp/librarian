# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class HeaderElement(WLElement):
    NUMBERING = 'i'
    HTML_TAG = 'span'
    FB2_TAG = 'p'
    
    def txt_build(self, builder):
        builder.enter_fragment('header')
        super().txt_build(builder)
        builder.exit_fragment()

    def html_build(self, builder):
        builder.enter_fragment('header')
        super().html_build(builder)
        builder.exit_fragment()

    def fb2_build(self, builder):
        builder.enter_fragment('header')
        super().fb2_build(builder)
        builder.exit_fragment()
