from ..base import WLElement


class SekcjaSwiatlo(WLElement):
    TXT_BOTTOM_MARGIN = 6
    TXT_LEGACY_BOTTOM_MARGIN = 4

    HTML_TAG = "hr"
    HTML_CLASS = "spacer"

    EPUB_TAG = 'p'
    EPUB_CLASS = 'spacer'

    def _epub_build_inner(self, builder):
        builder.push_text("\u00a0")
