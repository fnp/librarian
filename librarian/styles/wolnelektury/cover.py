# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from PIL import Image, ImageFont, ImageDraw
from StringIO import StringIO
from librarian import get_resource, URLOpener
from librarian.cover import Cover, TextBox


class WLCover(Cover):
    """Default Wolne Lektury cover generator."""
    width = 600
    height = 833
    uses_dc_cover = True
    author_font = ImageFont.truetype(
        get_resource('fonts/JunicodeWL-Regular.ttf'), 20)
    author_lineskip = 30
    title_font = ImageFont.truetype(
        get_resource('fonts/DejaVuSerif-Bold.ttf'), 30)
    title_lineskip = 40
    title_box_width = 350
    bar_width = 35
    background_color = '#444'
    author_color = '#444'
    default_background = get_resource('res/cover.png')
    format = 'JPEG'

    epoch_colors = {
        u'Starożytność': '#9e3610',
        u'Średniowiecze': '#564c09',
        u'Renesans': '#8ca629',
        u'Barok': '#a6820a',
        u'Oświecenie': '#f2802e',
        u'Romantyzm': '#db4b16',
        u'Pozytywizm': '#961060',
        u'Modernizm': '#7784e0',
        u'Dwudziestolecie międzywojenne': '#3044cf',
        u'Współczesność': '#06393d',
    }

    def __init__(self, book_info, format=None, image_cache=None):
        super(WLCover, self).__init__(book_info, format=format)
        self.kind = book_info.kind
        self.epoch = book_info.epoch
        if book_info.cover_url:
            url = book_info.cover_url
            bg_src = None
            if image_cache:
                from urllib import quote
                try:
                    bg_src = URLOpener().open(image_cache + quote(url, safe=""))
                except:
                    pass
            if bg_src is None:
                bg_src = URLOpener().open(url)
            self.background_img = StringIO(bg_src.read())
            bg_src.close()
        else:
            self.background_img = self.default_background

    def pretty_author(self):
        return self.author.upper()

    def image(self):
        img = Image.new('RGB', (self.width, self.height), self.background_color)
        draw = ImageDraw.Draw(img)

        if self.epoch in self.epoch_colors:
            epoch_color = self.epoch_colors[self.epoch]
        else:
            epoch_color = '#000'
        draw.rectangle((0, 0, self.bar_width, self.height), fill=epoch_color)

        if self.background_img:
            src = Image.open(self.background_img)
            trg_size = (self.width - self.bar_width, self.height)
            if src.size[0] * trg_size[1] < src.size[1] * trg_size[0]:
                resized = (
                    trg_size[0],
                    src.size[1] * trg_size[0] / src.size[0]
                )
                cut = (resized[1] - trg_size[1]) / 2
                src = src.resize(resized)
                src = src.crop((0, cut, src.size[0], src.size[1] - cut))
            else:
                resized = (
                    src.size[0] * trg_size[1] / src.size[1],
                    trg_size[1],
                )
                cut = (resized[0] - trg_size[0]) / 2
                src = src.resize(resized)
                src = src.crop((cut, 0, src.size[0] - cut, src.size[1]))

            img.paste(src, (self.bar_width, 0))
            del src

        box = TextBox(self.title_box_width, self.height, padding_y=20)
        box.text(self.pretty_author(),
                 font=self.author_font,
                 line_height=self.author_lineskip,
                 color=self.author_color,
                 shadow_color=self.author_shadow)

        box.skip(10)
        box.draw.line((75, box.height, 275, box.height), fill=self.author_color, width=2)
        box.skip(15)

        box.text(self.pretty_title(),
                 line_height=self.title_lineskip,
                 font=self.title_font,
                 color=epoch_color,
                 shadow_color=self.title_shadow)
        box_img = box.image()

        if self.kind == 'Liryka':
            # top
            box_top = 100
        elif self.kind == 'Epika':
            # bottom
            box_top = self.height - 100 - box_img.size[1]
        else:
            # center
            box_top = (self.height - box_img.size[1]) / 2

        box_left = self.bar_width + (self.width - self.bar_width - box_img.size[0]) / 2
        draw.rectangle((
            box_left, box_top,
            box_left + box_img.size[0], box_top + box_img.size[1]),
            fill='#fff')
        img.paste(box_img, (box_left, box_top), box_img)

        return img
