from ..base import WLElement


class Numeracja(WLElement):
    pass


class Rownolegle(WLElement):
    def build_epub(self, builder):
        for i, block in enumerate(self):
            attr = {"class": "rownolegly-blok"}
            if not i:
                attr['class'] += ' first'
            if i == len(self) - 1:
                attr['class'] += ' last'
            builder.start_element('div', attr)
            self.build_epub(block, builder)
            builder.end_element()


class Tab(WLElement):
    EPUB_TAG = HTML_TAG = 'span'

    def get_html_attr(self, builder):
        try:
            szer = int(self.get('szer', 1))
        except:
            szer = 1
        return {
            "display": "inline-block",
            "width": f"{szer}em",
        }

    get_epub_attr = get_html_attr

