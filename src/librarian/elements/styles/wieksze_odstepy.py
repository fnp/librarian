from ..base import WLElement


class WiekszeOdstepy(WLElement):
    TXT_PREFIX = "*"
    TXT_SUFFIX = "*"

    EPUB_TAG = HTML_TAG = "em"
    EPUB_CLASS = HTML_CLASS = "wieksze-odstepy"
