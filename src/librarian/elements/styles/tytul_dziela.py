# -*- coding: utf-8
from ..base import WLElement


class TytulDziela(WLElement):
    def normalize_text(self, text):
        txt = super(TytulDziela, self).normalize_text(text)
        if self.attrib.get('typ') == '1':
            txt = '„{txt}”'.format(txt=txt)
        return txt
