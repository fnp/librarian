from ..base import WLElement


class ListaOsoba(WLElement):
    TXT_TOP_MARGIN = 1
    TXT_BOTTOM_MARGIN = 1
    TXT_LEGACY_TOP_MARGIN = 1
    TXT_LEGACY_BOTTOM_MARGIN = 0
    TXT_PREFIX = " * "

    HTML_TAG = "li"

    def html_build(self, builder):
        builder.enter_fragment('list')
        super(ListaOsoba, self).html_build(builder)
        builder.exit_fragment()
        
