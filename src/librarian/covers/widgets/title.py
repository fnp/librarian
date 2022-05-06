import PIL.ImageFont
from librarian import get_resource
from librarian.cover import Metric
from ..utils.textbox import TextBox, split_words
from .base import Widget


class TitleBox(Widget):
    font_size = 159 # 45pt
    leading = 176  # 50pt
    tracking = 2.385

    def __init__(self, cover, width, height, lines, force=False):
        self.width = width
        self.height = height
        self.lines = lines
        self.force = force
        self.m = Metric(self, cover.m._scale)
        super().__init__(cover)

    def setup(self):
        m = self.m
        while True:
            try:
                self.build_box()
            except:
                if self.force:
                    self.m = Metric(self, self.m._scale * .99)
                    print('lower to', self.m.font_size)
                else:
                    raise
            else:
                break

    def build_box(self):
        title_font = PIL.ImageFont.truetype(
            get_resource('fonts/SourceSans3VF-Roman.ttf'),
            self.m.font_size,
            layout_engine=PIL.ImageFont.LAYOUT_BASIC
        )
        title_font.set_variation_by_axes([800])

        lines = self.lines or (int(self.height * (176/200) / self.m.leading) - 0)
        
        self.tb = TextBox(
            self.width,
            self.height,
            split_words(self.cover.title),
            title_font,
            lines,
            self.m.leading,
            self.m.tracking,
            .5, .5
        )
        self.margin_top = self.tb.margin_top
            
    def build(self, w, h):
        return self.tb.as_pil_image(self.cover.color_scheme['text'])

