# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class Numeracja(WLElement):
    NUMBERING = True
    def assign_id(self, builder):
        builder.counters['_visible'] = int(self.get('start', 1))


class Rownolegle(WLElement):
    def epub_build(self, builder):
        for i, block in enumerate(self):
            attr = {"class": "rownolegly-blok"}
            if not i:
                attr['class'] += ' first'
            if i == len(self) - 1:
                attr['class'] += ' last'
            builder.start_element('div', attr)
            block.epub_build(builder)
            builder.end_element()

    def html_build(self, builder):
        for i, block in enumerate(self):
            attr = {"class": "paralell-block"}
            if not i:
                attr['class'] += ' paralell-block-first'
            if i == len(self) - 1:
                attr['class'] += ' paralell-block-last'
            builder.start_element('div', attr)
            block.html_build(builder)
            builder.end_element()



class Tab(WLElement):
    EPUB_TAG = HTML_TAG = 'span'

    def html_build(self, builder):
        szer = self.get('szer', '1')
        if szer == '*':
            reopen = []
            from lxml import etree
            p = builder.cursor
            while 'verse' not in p.attrib.get('class', ''):
                reopen.append(p)
                p = p.getparent()
                builder.end_element()
            builder.start_element('span', {'class': 'verse-stretched-space'})
            builder.end_element()
            while reopen:
                p = reopen.pop()
                builder.start_element(p.tag, p.attrib)
        else:
            super().html_build(builder)

    def get_html_attr(self, builder):
        szer = self.get('szer', '1').strip()
        if szer.endswith('em'):
            szer = szer[:-2]
        try:
            szer = int(szer)
        except:
            szer = 1
        return {
            "display": "inline-block",
            "width": f"{szer}em",
        }

    get_epub_attr = get_html_attr

    def txt_build(self, builder):
        szer = self.get('szer', '1').strip()
        if szer.endswith('em'):
            szer = szer[:-2]
        try:
            szer = int(szer)
        except:
            szer = 1
        builder.push_text(' ' * 4 * szer)
