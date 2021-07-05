from ..base import WLElement


class Motto(WLElement):
    TXT_LEGACY_TOP_MARGIN = 4
    TXT_LEGACY_BOTTOM_MARGIN = 2

    EPUB_TAG = HTML_TAG = "div"
    EPUB_CLASS = HTML_CLASS = "motto"
