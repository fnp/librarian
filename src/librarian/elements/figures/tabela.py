from ..base import WLElement


class Tabela(WLElement):
    HTML_TAG = 'table'

    def get_html_attr(self, builder):
        if self.attrib.get('ramka', '') == '1':
            return {
                'class': 'border'
            }
        return {}
