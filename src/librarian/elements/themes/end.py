from ..base import WLElement


class End(WLElement):
    HTML_TAG = 'span'

    def get_html_attr(self, builder):
        fid = self.attrib.get('id', '')[1:]
        return {
            "class": "theme-end",
            "fid": fid
        }
