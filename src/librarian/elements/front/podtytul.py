from .base import HeaderElement


class Podtytul(HeaderElement):
    TXT_BOTTOM_MARGIN = 1
    TXT_LEGACY_BOTTOM_MARGIN = 1

    HTML_CLASS = 'subtitle'

    EPUB_TAG = 'h2'
    EPUB_CLASS = 'insubtitle'

