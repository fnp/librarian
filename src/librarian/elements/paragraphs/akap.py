from ..base import WLElement


class Akap(WLElement):
    STRIP = True

    TXT_TOP_MARGIN = 2
    TXT_BOTTOM_MARGIN = 2
    TXT_LEGACY_TOP_MARGIN = 2
    TXT_LEGACY_BOTTOM_MARGIN = 0

    HTML_TAG = 'p'
    HTML_CLASS = 'paragraph'

    HTML_SECTION = True
