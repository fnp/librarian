from ..base import WLElement


class PoezjaCyt(WLElement):
    CAN_HAVE_TEXT = False

    TXT_TOP_MARGIN = 3
    TXT_BOTTOM_MARGIN = 3
    TXT_LEGACY_TOP_MARGIN = 1
    TXT_LEGACY_BOTTOM_MARGIN = 0

    HTML_TAG = 'blockquote'

    EPUB_TAG = 'div'
    EPUB_CLASS = 'block'
