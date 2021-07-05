from ..base import WLElement


class Kwestia(WLElement):
    CAN_HAVE_TEXT = False

    EPUB_TAG = HTML_TAG = "div"
    EPUB_CLASS = HTML_CLASS = "kwestia"
