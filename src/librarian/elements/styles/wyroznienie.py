from ..base import WLElement


class Wyroznienie(WLElement):
    TXT_PREFIX = "*"
    TXT_SUFFIX = "*"

    EPUB_TAG = HTML_TAG = "em"
    EPUB_CLASS = HTML_CLASS = "author-emphasis"
