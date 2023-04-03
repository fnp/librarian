from ..base import WLElement


class NaglowekCzesc(WLElement):
    SECTION_PRECEDENCE = 1
    SHOULD_HAVE_ID = True
    
    TXT_TOP_MARGIN = 5
    TXT_BOTTOM_MARGIN = 2
    TXT_LEGACY_TOP_MARGIN = 5
    TXT_LEGACY_BOTTOM_MARGIN = 0

    EPUB_TAG = HTML_TAG = "h2"

    EPUB_CLASS = "h2"
    EPUB_START_CHUNK = True
