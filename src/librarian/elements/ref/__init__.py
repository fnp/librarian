from ..base import WLElement


class Ref(WLElement):
    ASIDE = True
    HTML_TAG = 'a'
    
    def txt_build(self, builder):
        pass

    def get_html_attr(self, builder):
        return {
            'class': 'reference',
            'data-uri': self.attrib.get('href', ''),
        }

    def epub_build(self, builder):
        pass
