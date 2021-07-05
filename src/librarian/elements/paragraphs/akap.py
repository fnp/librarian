from ..base import WLElement


class Akap(WLElement):
    STRIP = True

    TXT_TOP_MARGIN = 2
    TXT_BOTTOM_MARGIN = 2
    TXT_LEGACY_TOP_MARGIN = 2
    TXT_LEGACY_BOTTOM_MARGIN = 0

    EPUB_TAG = HTML_TAG = 'p'
    EPUB_CLASS = HTML_CLASS = 'paragraph'
