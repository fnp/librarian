from ..base import WLElement


class Werset(WLElement):
    STRIP = True
    NUMBERING = 'main'

    TXT_TOP_MARGIN = 1
    TXT_BOTTOM_MARGIN = 1

    EPUB_TAG = HTML_TAG = 'div'
    EPUB_CLASS = 'verse-relig'
    HTML_CLASS = 'wl verse-relig'

    has_visible_numbering = True

    def epub_build_inner(self, builder):
        builder.numbering += 1
        builder.push_text(str(builder.numbering))


class Petucha(WLElement):
    HTML_TAG = EPUB_TAG = 'span'
    HTML_CLASS = EPUB_CLASS = 'petucha'

    def html_build_inner(self, builder):
        builder.push_text('{פ}')


class Stuma(WLElement):
    HTML_TAG = EPUB_TAG = 'span'
    HTML_CLASS = EPUB_CLASS = 'stuma'

    def html_build_inner(self, builder):
        builder.push_text('{ס}')
