from ..base import WLElement


class NaglowekPodrozdzial(WLElement):
    SECTION_PRECEDENCE = 3
    SHOULD_HAVE_ID = True

    TXT_TOP_MARGIN = 3
    TXT_BOTTOM_MARGIN = 2
    TXT_LEGACY_TOP_MARGIN = 3
    TXT_LEGACY_BOTTOM_MARGIN = 0

    HTML_TAG = "h4"

    EPUB_TAG = "h2"
    EPUB_CLASS = "h4"
