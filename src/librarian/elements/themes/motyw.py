from ..base import WLElement


class Motyw(WLElement):
    ASIDE = True
    HTML_TAG = "a"

    def txt_build(self, builder):
        pass

    def html_build(self, builder):
        if builder.with_themes:
            super(Motyw, self).html_build(builder)

    def get_html_attr(self, builder):
        fid = self.attrib.get('id', '')[1:]
        return {
            "class": "theme-begin",
            "fid": fid,
            "name": "m" + fid,
        }

    def epub_build(self, builder):
        pass
