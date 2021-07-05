from .base import HeaderElement


class NazwaUtworu(HeaderElement):
    TXT_BOTTOM_MARGIN = 1
    TXT_LEGACY_BOTTOM_MARGIN = 1

    HTML_CLASS = 'title'

    EPUB_TAG = 'h2'
    EPUB_CLASS = 'intitle'
