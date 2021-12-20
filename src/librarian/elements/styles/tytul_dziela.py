# -*- coding: utf-8
from ..base import WLElement


class TytulDziela(WLElement):
    EPUB_TAG = HTML_TAG = 'em'
    EPUB_CLASS = HTML_CLASS = 'book-title'

    def normalize_text(self, text, builder):
        txt = super(TytulDziela, self).normalize_text(text, builder)
        if self.attrib.get('typ') == '1':
            txt = '„{txt}”'.format(txt=txt)
        return txt
