# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class Numeracja(WLElement):
    def build_epub(self, builder):
        builder.numbering = 0


class Rownolegle(WLElement):
    def build_epub(self, builder):
        for i, block in enumerate(self):
            attr = {"class": "rownolegly-blok"}
            if not i:
                attr['class'] += ' first'
            if i == len(self) - 1:
                attr['class'] += ' last'
            builder.start_element('div', attr)
            self.build_epub(block, builder)
            builder.end_element()


class Tab(WLElement):
    EPUB_TAG = HTML_TAG = 'span'

    def get_html_attr(self, builder):
        try:
            szer = int(self.get('szer', 1))
        except:
            szer = 1
        return {
            "display": "inline-block",
            "width": f"{szer}em",
        }

    get_epub_attr = get_html_attr


class Audio(WLElement):
    def build_epub(self, builder):
        return


class Br(WLElement):
    TXT_SUFFIX = "\n"
    EPUB_TAG = HTML_TAG = "br"
