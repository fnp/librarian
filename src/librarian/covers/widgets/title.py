# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import PIL.ImageFont
from librarian import get_resource
from librarian.cover import Metric
from ..utils.textbox import TextBox, split_words
from .base import Widget


class TitleBox(Widget):
    font_size = 159 # 45pt
    leading = 176  # 50pt
    tracking = 2.385

    def __init__(self, cover, width, height, lines, scale=1):
        self.width = width
        self.height = height
        self.lines = lines
        self.m = Metric(self, cover.m._scale * scale)
        super().__init__(cover)

    def setup(self):
        title_font = PIL.ImageFont.truetype(
            get_resource('fonts/SourceSans3VF-Roman.ttf'),
            self.m.font_size,
            layout_engine=PIL.ImageFont.Layout.BASIC
        )
        title_font.set_variation_by_axes([800])
        title_font_2 = PIL.ImageFont.truetype(
            get_resource('fonts/OpenSans-VariableFont_wdth,wght.ttf'),
            self.m.font_size,
            layout_engine=PIL.ImageFont.Layout.BASIC
        )
        title_font_2.set_variation_by_axes([700, 700])
        font_fallbacks = {
            ('\u0590', '\u05FF'): title_font_2,
        }

        lines = self.lines or (int(self.height * (176/200) / self.m.leading) - 0)
        
        self.tb = TextBox(
            self.width,
            self.height,
            split_words(self.cover.title),
            title_font,
            lines,
            self.m.leading,
            self.m.tracking,
            .5, .5,
            font_fallbacks=font_fallbacks
        )
        self.margin_top = self.tb.margin_top
            
    def build(self, w, h):
        return self.tb.as_pil_image(self.cover.color_scheme['text'])

