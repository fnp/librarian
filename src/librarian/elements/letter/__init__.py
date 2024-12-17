from ..base import WLElement


class List(WLElement):
    CAN_HAVE_TEXT = False

    TXT_TOP_MARGIN = 3
    TXT_BOTTOM_MARGIN = 2
    TXT_LEGACY_TOP_MARGIN = 1
    TXT_LEGACY_BOTTOM_MARGIN = 0

    HTML_TAG = 'blockquote'

    EPUB_TAG = 'div'
    EPUB_CLASS = 'block'


class Adresat(WLElement):
    STRIP = True
    SHOULD_HAVE_ID = True

    TXT_TOP_MARGIN = 2
    TXT_BOTTOM_MARGIN = 2
    TXT_LEGACY_TOP_MARGIN = 2
    TXT_LEGACY_BOTTOM_MARGIN = 0

    EPUB_TAG = HTML_TAG = 'p'
    EPUB_CLASS = HTML_CLASS = 'paragraph adresat'

class MiejsceData(WLElement):
    STRIP = True
    SHOULD_HAVE_ID = True

    TXT_TOP_MARGIN = 2
    TXT_BOTTOM_MARGIN = 2
    TXT_LEGACY_TOP_MARGIN = 2
    TXT_LEGACY_BOTTOM_MARGIN = 0

    EPUB_TAG = HTML_TAG = 'p'
    EPUB_CLASS = HTML_CLASS = 'paragraph miejscedata'

class NaglowekListu(WLElement):
    STRIP = True
    SHOULD_HAVE_ID = True

    TXT_TOP_MARGIN = 2
    TXT_BOTTOM_MARGIN = 2
    TXT_LEGACY_TOP_MARGIN = 2
    TXT_LEGACY_BOTTOM_MARGIN = 0

    EPUB_TAG = HTML_TAG = 'p'
    EPUB_CLASS = HTML_CLASS = 'paragraph nagloweklistu'

class Pozdrowienie(WLElement):
    STRIP = True
    SHOULD_HAVE_ID = True

    TXT_TOP_MARGIN = 2
    TXT_BOTTOM_MARGIN = 2
    TXT_LEGACY_TOP_MARGIN = 2
    TXT_LEGACY_BOTTOM_MARGIN = 0

    EPUB_TAG = HTML_TAG = 'p'
    EPUB_CLASS = HTML_CLASS = 'paragraph pozdrowienie'

class Podpis(WLElement):
    STRIP = True
    SHOULD_HAVE_ID = True

    TXT_TOP_MARGIN = 2
    TXT_BOTTOM_MARGIN = 2
    TXT_LEGACY_TOP_MARGIN = 2
    TXT_LEGACY_BOTTOM_MARGIN = 0

    EPUB_TAG = HTML_TAG = 'p'
    EPUB_CLASS = HTML_CLASS = 'paragraph podpis'
