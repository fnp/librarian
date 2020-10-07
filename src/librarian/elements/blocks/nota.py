from ..base import WLElement


class Nota(WLElement):
    CAN_HAVE_TEXT = False

    HTML_TAG = "div"
    HTML_CLASS = "note"
