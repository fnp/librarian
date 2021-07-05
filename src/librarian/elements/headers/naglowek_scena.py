from ..base import WLElement


class NaglowekScena(WLElement):
    SECTION_PRECEDENCE = 2

    TXT_TOP_MARGIN = 4
    TXT_BOTTOM_MARGIN = 2
    TXT_LEGACY_TOP_MARGIN = 4
    TXT_LEGACY_BOTTOM_MARGIN = 0

    HTML_TAG = 'h3'

    EPUB_TAG = 'h2'
    EPUB_CLASS = 'h3'
    EPUB_START_CHUNK = False

