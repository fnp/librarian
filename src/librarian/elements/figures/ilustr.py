from ..base import WLElement


class Ilustr(WLElement):
    HTML_TAG = 'img'

    def get_html_attr(self, builder):
        return {
            'src': builder.base_url + self.attrib['src'],
            'alt': self.attrib['alt'],
            'title': self.attrib['alt'],
        }
