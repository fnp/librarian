from ..base import WLElement


class WWW(WLElement):
    EPUB_TAG = 'a'

    def get_epub_attr(self, builder):
        attr = super().get_epub_attr(builder)
        attr['href'] = self.text
        return attr

