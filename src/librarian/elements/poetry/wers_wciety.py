from .wers import Wers


class WersWciety(Wers):
    @property
    def typ(self):
        v = self.attrib.get('typ')
        return int(v) if v else 1

    def _txt_build_inner(self, builder):
        ## Temporary legacy compatibility fix.
        typ = min(self.typ, 2)

        builder.push_text('  ' * self.typ, prepared=True)
        super(WersWciety, self)._txt_build_inner(builder)

    def get_html_attr(self, builder):
        attr = super(WersWciety, self).get_html_attr(builder)
        attr['style'] = "padding-left: {}em".format(self.typ)
        return attr

    def get_epub_attr(self, builder):
        attr = super(WersWciety, self).get_html_attr(builder)
        attr['style'] = "margin-left: {}em".format(self.typ)
        return attr
