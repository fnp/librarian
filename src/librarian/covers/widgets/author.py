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

        if authors and translators:
            # Try with two boxes.

            authors_shortened = False
            author_box = None
            while author_box is None:
                author_str = ', '.join(authors)
                if authors_shortened:
                    # translate!
                    author_str += ' i in.'
                try:
                    author_box = TextBox(
                        self.width,
                        self.m.leading * 2,
                        [author_str],
                        author_font,
                        1,
                        self.m.leading,
                        0,
                        1, 0
                    )
                except DoesNotFit:
                    authors.pop()
                    authors_shortened = True

            translators_shortened = False
            translator_box = None
            while translator_box is None:
                translator_str = '(tłum. ' + ', '.join(translators)
                if translators_shortened:
                    translator_str += ' i in.'
                translator_str += ')'
                try:
                    translator_box = TextBox(
                        self.width,
                        self.m.leading * 2,
                        [translator_str],
                        translator_font,
                        1,
                        self.m.leading,
                        0,
                        1, 0
                    )
                except DoesNotFit:
                    translators.pop()
                    translators_shortened = True

            self.textboxes = [
                author_box,
                translator_box
            ]

        elif authors:
            author_box = None
            shortened = False
            while author_box is None:
                if not shortened and len(authors) == 2:
                    parts = authors
                elif len(authors) > 2:
                    parts = [author + ',' for author in authors[:-1]] + [authors[-1]]
                    if shortened:
                        parts.append('i in.')
                else:
                    parts = split_words(authors[0])
                    if shortened:
                        parts.append('i in.')

                try:
                    if len(parts) > 1:
                        # Author in two lines.
                        author_box = TextBox(
                            self.width,
                            self.m.leading * 2,
                            parts,
                            author_font,
                            2,
                            self.m.leading,
                            0,
                            1, 0
                        )
                    else:
                        # author in one line.
                        author_box = TextBox(
                            self.width,
                            self.m.leading * 2,
                            parts,
                            author_font,
                            1,
                            self.m.leading,
                            0,
                            1, 0
                        )
                except DoesNotFit:
                    authors.pop()
                    shortened = True

            self.textboxes = [author_box]

        self.margin_top = self.textboxes[0].margin_top

    def build(self, w, h):
        img = PIL.Image.new('RGBA', (self.width, self.m.leading * 2))
        offset = 0
        for i, tb in enumerate(self.textboxes):
            sub_img = tb.as_pil_image(self.cover.color_scheme['text'])
            img.paste(sub_img, (0, self.m.leading * i), sub_img)
        
        return img
