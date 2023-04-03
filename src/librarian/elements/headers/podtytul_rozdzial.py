from ..base import WLElement


class PodtytulRozdzial(WLElement):
    SHOULD_HAVE_ID = True

    TXT_TOP_MARGIN = 2
    TXT_BOTTOM_MARGIN = 2

    HTML_TAG = "div"
    HTML_CLASS = "subtitle3"

    EPUB_TAG = "h2"
    EPUB_CLASS = "h3"

    def _epub_build_inner(self, builder):
        builder.start_element('small', {})
        super()._epub_build_inner(builder)
        builder.end_element()
