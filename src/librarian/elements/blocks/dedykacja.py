from ..base import WLElement


class Dedykacja(WLElement):
    TXT_LEGACY_TOP_MARGIN = 2

    EPUB_TAG = HTML_TAG = "div"
    EPUB_CLASS = HTML_CLASS = "dedication"
