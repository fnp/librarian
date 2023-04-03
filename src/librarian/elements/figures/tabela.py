from ..base import WLElement


class Tabela(WLElement):
    SHOULD_HAVE_ID = True

    EPUB_TAG = HTML_TAG = 'table'

    def get_html_attr(self, builder):
        if self.attrib.get('ramka', '') == '1':
            return {
                'class': 'border'
            }
        return {}

    get_epub_attr = get_html_attr

                
