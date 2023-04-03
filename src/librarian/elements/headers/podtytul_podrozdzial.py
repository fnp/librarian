from ..base import WLElement


class PodtytulPodrozdzial(WLElement):
    SHOULD_HAVE_ID = True

    TXT_TOP_MARGIN = 2
    TXT_BOTTOM_MARGIN = 2

    HTML_TAG = "div"
    HTML_CLASS = "subtitle4"

    EPUB_TAG = "h2"
    EPUB_CLASS = "h4"

    def _epub_build_inner(self, builder):
        builder.start_element('small', {})
        super()._epub_build_inner(builder)
        builder.end_element()
