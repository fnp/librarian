from ..base import WLElement


class Ilustr(WLElement):
    HTML_TAG = 'img'

    def get_html_attr(self, builder):
        return {
            'src': builder.image_location + self.attrib['src']
        }
