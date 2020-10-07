from ..base import WLElement


class Motyw(WLElement):
    HTML_TAG = "a"

    def txt_build(self, builder):
        pass

    def get_html_attr(self, builder):
        fid = self.attrib['id'][1:]
        return {
            "class": "theme-begin",
            "fid": fid,
            "name": "m" + fid,
        }
