# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from .wers import Wers


class WersWciety(Wers):
    HTML_CLASS = Wers.HTML_CLASS + ' verse-indent'

    @property
    def typ(self):
        v = self.attrib.get('typ')
        return int(v) if v else 1

    def txt_build_inner(self, builder):
        ## Temporary legacy compatibility fix.
        typ = min(self.typ, 2)

        builder.push_text('  ' * self.typ, prepared=True)
        super().txt_build_inner(builder)

    def get_html_attr(self, builder):
        attr = super().get_html_attr(builder)
        attr['class'] += f" verse-indent-{self.typ}"
        return attr

    def get_epub_attr(self, builder):
        attr = super().get_html_attr(builder)
        attr['style'] = "margin-left: {}em".format(self.typ)
        return attr
