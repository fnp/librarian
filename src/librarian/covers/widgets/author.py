import PIL.ImageFont
from librarian import get_resource
from librarian.cover import Metric
from ..utils.textbox import TextBox, DoesNotFit, split_words
from .base import Widget


class AuthorBox(Widget):
    font_size = 75
    leading = 92

    def __init__(self, cover, width):
        self.width = width
        self.m = Metric(self, cover.m._scale)
        super().__init__(cover)

    def setup(self):
        author_font = PIL.ImageFont.truetype(
            get_resource('fonts/SourceSans3VF-Roman.ttf'),
            self.m.font_size,
            layout_engine=PIL.ImageFont.LAYOUT_BASIC
        )
        author_font.set_variation_by_axes([600])

        translator_font = PIL.ImageFont.truetype(
            get_resource('fonts/SourceSans3VF-Roman.ttf'),
            self.m.font_size,
            layout_engine=PIL.ImageFont.LAYOUT_BASIC
        )
        translator_font.set_variation_by_axes([400])

        authors = [a.readable() for a in self.cover.book_info.authors]
        translators = [a.readable() for a in self.cover.book_info.translators]

        authors_written = False
        if authors and translators:
            author_str = ', '.join(authors)
            translator_str = '(tłum. ' + ', '.join(translators) + ')'
            # just print
            parts = [author_str, translator_str]

            try:
                self.textboxes = [
                    TextBox(
                        self.width,
                        self.m.leading * 2,
                        [author_str],
                        author_font,
                        1,
                        self.m.leading,
                        0,
                        1, 0
                    ),
                    TextBox(
                        self.width,
                        self.m.leading * 2,
                        [translator_str],
                        translator_font,
                        1,
                        self.m.leading,
                        0,
                        1, 0
                    )
                ]
            except DoesNotFit:
                pass
            else:
                authors_written = True

        if not authors_written:
            assert authors
            if len(authors) == 2:
                parts = authors
            elif len(authors) > 2:
                parts = [author + ',' for author in authors[:-1]] + [authors[-1]]
            else:
                parts = split_words(authors[0])

            try:
                self.textboxes = [
                    TextBox(
                        self.width,
                        self.m.leading * 2,
                        parts,
                        author_font,
                        2,
                        self.m.leading,
                        0,
                        1, 0
                    )
                ]
            except:
                self.textboxes = [
                    TextBox(
                        self.width,
                        self.m.leading * 2,
                        parts,
                        author_font,
                        1,
                        self.m.leading,
                        0,
                        1, 0
                    )
                ]
        self.margin_top = self.textboxes[0].margin_top

    def build(self, w, h):
        img = PIL.Image.new('RGBA', (self.width, self.m.leading * 2))
        offset = 0
        for i, tb in enumerate(self.textboxes):
            sub_img = tb.as_pil_image(self.cover.color_scheme['text'])
            img.paste(sub_img, (0, self.m.leading * i), sub_img)
        
        return img
