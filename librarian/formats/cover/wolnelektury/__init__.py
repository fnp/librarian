# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from PIL import Image, ImageFont, ImageDraw
from librarian.utils import get_resource
from .. import Cover, Metric, TextBox


class WLCover(Cover):
    """Default Wolne Lektury cover generator."""
    format_name = u"WL-style cover image"

    width = 600
    height = 833
    uses_dc_cover = True
    author_font_ttf = get_resource('fonts/JunicodeWL-Regular.ttf')
    author_font_size = 20
    author_lineskip = 30
    title_font_ttf = get_resource('fonts/DejaVuSerif-Bold.ttf')
    title_font_size = 30
    title_lineskip = 40
    title_box_width = 350
    
    box_top_margin = 100
    box_bottom_margin = 100
    box_padding_y = 20
    box_above_line = 10
    box_below_line = 15
    box_line_left = 75
    box_line_right = 275
    box_line_width = 2

    logo_top = 15
    logo_width = 140

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

    def __init__(self, doc, format=None, width=None, height=None, with_logo=False):
        super(WLCover, self).__init__(doc, format=format, width=width, height=height)
        self.kind = doc.meta.get_one('kind')
        self.epoch = doc.meta.get_one('epoch')
        self.with_logo = with_logo
        # TODO
        if doc.meta.get('cover_url'):
            url = doc.meta.get('cover_url')[0]
            bg_src = None
            if bg_src is None:
                bg_src = URLOpener().open(url)
            self.background_img = StringIO(bg_src.read())
            bg_src.close()
        else:
            self.background_img = self.default_background

    def pretty_author(self):
        return self.author.upper()

    def image(self):
        metr = Metric(self, self.scale)
        img = Image.new('RGB', (metr.width, metr.height), self.background_color)
        draw = ImageDraw.Draw(img)

        if self.epoch in self.epoch_colors:
            epoch_color = self.epoch_colors[self.epoch]
        else:
            epoch_color = '#000'
        draw.rectangle((0, 0, metr.bar_width, metr.height), fill=epoch_color)

        if self.background_img:
            src = Image.open(self.background_img)
            trg_size = (metr.width - metr.bar_width, metr.height)
            if src.size[0] * trg_size[1] < src.size[1] * trg_size[0]:
                resized = (
                    trg_size[0],
                    src.size[1] * trg_size[0] / src.size[0]
                )
                cut = (resized[1] - trg_size[1]) / 2
                src = src.resize(resized, Image.ANTIALIAS)
                src = src.crop((0, cut, src.size[0], src.size[1] - cut))
            else:
                resized = (
                    src.size[0] * trg_size[1] / src.size[1],
                    trg_size[1],
                )
                cut = (resized[0] - trg_size[0]) / 2
                src = src.resize(resized, Image.ANTIALIAS)
                src = src.crop((cut, 0, src.size[0] - cut, src.size[1]))

            img.paste(src, (metr.bar_width, 0))
            del src

        box = TextBox(metr.title_box_width, metr.height, padding_y=metr.box_padding_y)
        author_font = ImageFont.truetype(
            self.author_font_ttf, metr.author_font_size)
        box.text(self.pretty_author(),
                 font=author_font,
                 line_height=metr.author_lineskip,
                 color=self.author_color,
                 shadow_color=self.author_shadow,
                )

        box.skip(metr.box_above_line)
        box.draw.line((metr.box_line_left, box.height, metr.box_line_right, box.height),
                fill=self.author_color, width=metr.box_line_width)
        box.skip(metr.box_below_line)

        title_font = ImageFont.truetype(
            self.title_font_ttf, metr.title_font_size)
        box.text(self.pretty_title(),
                 line_height=metr.title_lineskip,
                 font=title_font,
                 color=epoch_color,
                 shadow_color=self.title_shadow,
                )

        if self.with_logo:
            logo = Image.open(get_resource('res/wl-logo-mono.png'))
            logo = logo.resize((metr.logo_width, logo.size[1] * metr.logo_width / logo.size[0]), Image.ANTIALIAS)
            alpha = logo.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(.75)
            logo.putalpha(alpha)
            box.skip(metr.logo_top + logo.size[1])

        box_img = box.image()

        if self.kind == 'Liryka':
            # top
            box_top = metr.box_top_margin
        elif self.kind == 'Epika':
            # bottom
            box_top = metr.height - metr.box_bottom_margin - box_img.size[1]
        else:
            # center
            box_top = (metr.height - box_img.size[1]) / 2

        box_left = metr.bar_width + (metr.width - metr.bar_width -
                        box_img.size[0]) / 2
        draw.rectangle((box_left, box_top,
            box_left + box_img.size[0], box_top + box_img.size[1]),
            fill='#fff')
        img.paste(box_img, (box_left, box_top), box_img)

        if self.with_logo:
            img.paste(logo, 
                (box_left + (box_img.size[0] - logo.size[0]) / 2,
                    box_top + box_img.size[1] - metr.box_padding_y - logo.size[1]), mask=logo)

        return img
