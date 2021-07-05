from ..base import WLElement


class Nota(WLElement):
    CAN_HAVE_TEXT = False

    EPUB_TAG = HTML_TAG = "div"
    EPUB_CLASS = HTML_CLASS = "note"
