# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from lxml import etree
from ..base import WLElement


class ListaOsob(WLElement):
    NUMBERING = 'i'
    CAN_HAVE_TEXT = False

    TXT_TOP_MARGIN = 3
    TXT_BOTTOM_MARGIN = 3

    HTML_TAG = "div"
    HTML_CLASS = "person-list"

    def html_build_inner(self, builder):
        ol = etree.Element('ol')
        builder.create_fragment('list', ol)
        super().html_build_inner(builder)
        builder.cursor.append(ol)
        builder.forget_fragment('list')

    def epub_build_inner(self, builder):
        ol = etree.Element('ol')
        builder.create_fragment('list', ol)
        super().epub_build_inner(builder)
        builder.cursor.append(ol)
        builder.forget_fragment('list')
