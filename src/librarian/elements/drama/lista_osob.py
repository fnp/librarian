from lxml import etree
from ..base import WLElement


class ListaOsob(WLElement):
    CAN_HAVE_TEXT = False
    SHOULD_HAVE_ID = True

    TXT_TOP_MARGIN = 3
    TXT_BOTTOM_MARGIN = 3
    TXT_LEGACY_TOP_MARGIN = 3
    TXT_LEGACY_BOTTOM_MARGIN = 1

    HTML_TAG = "div"
    HTML_CLASS = "person-list"

    def _html_build_inner(self, builder):
        ol = etree.Element('ol')
        builder.create_fragment('list', ol)
        super(ListaOsob, self)._html_build_inner(builder)
        builder.cursor.append(ol)
        builder.forget_fragment('list')

    def _epub_build_inner(self, builder):
        ol = etree.Element('ol')
        builder.create_fragment('list', ol)
        super(ListaOsob, self)._epub_build_inner(builder)
        builder.cursor.append(ol)
        builder.forget_fragment('list')
