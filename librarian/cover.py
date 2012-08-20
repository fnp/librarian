# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import re
import Image, ImageFont, ImageDraw, ImageFilter
from StringIO import StringIO
from librarian import get_resource, OutputFile


class TextBox(object):
    """Creates an Image with a series of centered strings."""

    SHADOW_X = 3
    SHADOW_Y = 3
    SHADOW_BLUR = 3

    def __init__(self, max_width, max_height, padding_x=None, padding_y=None):
        if padding_x is None:
            padding_x = self.SHADOW_X + self.SHADOW_BLUR
        if padding_y is None:
            padding_y = self.SHADOW_Y + self.SHADOW_BLUR

        self.max_width = max_width
        self.max_text_width = max_width - 2 * padding_x
        self.padding_y = padding_y
        self.height = padding_y
        self.img = Image.new('RGBA', (max_width, max_height))
        self.draw = ImageDraw.Draw(self.img)
        self.shadow_img = None
        self.shadow_draw = None

    def skip(self, height):
        """Skips some vertical space."""
        self.height += height

    def text(self, text, color='#000', font=None, line_height=20,
             shadow_color=None):
        """Writes some centered text."""
        text = re.sub(r'\s+', ' ', text)
        if shadow_color:
            if not self.shadow_img:
                self.shadow_img = Image.new('RGBA', self.img.size)
                self.shadow_draw = ImageDraw.Draw(self.shadow_img)
        while text:
            line = text
            line_width = self.draw.textsize(line, font=font)[0]
            while line_width > self.max_text_width:
                parts = line.rsplit(' ', 1)
                if len(parts) == 1:
                    line_width = self.max_text_width
                    break
                line = parts[0]
                line_width = self.draw.textsize(line, font=font)[0]
            line = line.strip() + ' '

            pos_x = (self.max_width - line_width) / 2

            if shadow_color:
                self.shadow_draw.text(
                        (pos_x + self.SHADOW_X, self.height + self.SHADOW_Y),
                        line, font=font, fill=shadow_color
                )

            self.draw.text((pos_x, self.height), line, font=font, fill=color)
            self.height += line_height
            # go to next line
            text = text[len(line):]

    def image(self):
        """Creates the actual Image object."""
        image = Image.new('RGBA', (self.max_width,
                                   self.height + self.padding_y))
        if self.shadow_img:
            shadow = self.shadow_img.filter(ImageFilter.BLUR)
            image.paste(shadow, (0, 0), shadow)
            image.paste(self.img, (0, 0), self.img)
        else:
            image.paste(self.img, (0, 0))
        return image


class Cover(object):
    """Abstract base class for cover images generator."""
    width = 600
    height = 800
    background_color = '#fff'
    background_img = None

    author_top = 100
    author_margin_left = 20
    author_margin_right = 20
    author_lineskip = 40
    author_color = '#000'
    author_shadow = None
    author_font = None

    title_top = 100
    title_margin_left = 20
    title_margin_right = 20
    title_lineskip = 54
    title_color = '#000'
    title_shadow = None
    title_font = None

    logo_bottom = None
    logo_width = None
    uses_dc_cover = False

    format = 'JPEG'

    exts = {
        'JPEG': 'jpg',
        'PNG': 'png',
        }

    mime_types = {
        'JPEG': 'image/jpeg',
        'PNG': 'image/png',
        }

    def __init__(self, book_info, format=None):
        self.author = ", ".join(auth.readable() for auth in book_info.authors)
        self.title = book_info.title
        if format is not None:
            self.format = format

    def pretty_author(self):
        """Allows for decorating author's name."""
        return self.author

    def pretty_title(self):
        """Allows for decorating title."""
        return self.title

    def image(self):
        img = Image.new('RGB', (self.width, self.height), self.background_color)

        if self.background_img:
            background = Image.open(self.background_img)
            img.paste(background, None, background)
            del background

        # WL logo
        if self.logo_width:
            logo = Image.open(get_resource('res/wl-logo.png'))
            logo = logo.resize((self.logo_width, logo.size[1] * self.logo_width / logo.size[0]))
            img.paste(logo, ((self.width - self.logo_width) / 2, img.size[1] - logo.size[1] - self.logo_bottom))

        top = self.author_top
        tbox = TextBox(
            self.width - self.author_margin_left - self.author_margin_right,
            self.height - top,
            )
        author_font = self.author_font or ImageFont.truetype(
            get_resource('fonts/DejaVuSerif.ttf'), 30)
        tbox.text(self.pretty_author(), self.author_color, author_font,
            self.author_lineskip, self.author_shadow)
        text_img = tbox.image()
        img.paste(text_img, (self.author_margin_left, top), text_img)

        top += text_img.size[1] + self.title_top
        tbox = TextBox(
            self.width - self.title_margin_left - self.title_margin_right,
            self.height - top,
            )
        title_font = self.author_font or ImageFont.truetype(
            get_resource('fonts/DejaVuSerif.ttf'), 40)
        tbox.text(self.pretty_title(), self.title_color, title_font,
            self.title_lineskip, self.title_shadow)
        text_img = tbox.image()
        img.paste(text_img, (self.title_margin_left, top), text_img)

        return img

    def mime_type(self):
        return self.mime_types[self.format]

    def ext(self):
        return self.exts[self.format]

    def save(self, *args, **kwargs):
        return self.image().save(format=self.format, *args, **kwargs)

    def output_file(self, *args, **kwargs):
        imgstr = StringIO()
        self.save(imgstr, *args, **kwargs)
        return OutputFile.from_string(imgstr.getvalue())


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
            from urllib2 import urlopen
            from StringIO import StringIO

            url = book_info.cover_url
            bg_src = None
            if image_cache:
                from urllib import quote
                try:
                    bg_src = urlopen(image_cache + quote(url, safe=""))
                except:
                    pass
            if bg_src is None:
                bg_src = urlopen(url)
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
                 shadow_color=self.author_shadow,
                )

        box.skip(10)
        box.draw.line((75, box.height, 275, box.height),
                fill=self.author_color, width=2)
        box.skip(15)

        box.text(self.pretty_title(),
                 line_height=self.title_lineskip,
                 font=self.title_font,
                 color=epoch_color,
                 shadow_color=self.title_shadow,
                )
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

        box_left = self.bar_width + (self.width - self.bar_width -
                        box_img.size[0]) / 2
        draw.rectangle((box_left, box_top,
            box_left + box_img.size[0], box_top + box_img.size[1]),
            fill='#fff')
        img.paste(box_img, (box_left, box_top), box_img)

        return img



class VirtualoCover(Cover):
    width = 600
    height = 730
    author_top = 73
    title_top = 73
    logo_bottom = 25
    logo_width = 250


class PrestigioCover(Cover):
    width = 580
    height = 783
    background_img = get_resource('res/cover-prestigio.png')

    author_top = 446
    author_margin_left = 118
    author_margin_right = 62
    author_lineskip = 60
    author_color = '#fff'
    author_shadow = '#000'
    author_font = ImageFont.truetype(get_resource('fonts/JunicodeWL-Italic.ttf'), 50)

    title_top = 0
    title_margin_left = 118
    title_margin_right = 62
    title_lineskip = 60
    title_color = '#fff'
    title_shadow = '#000'
    title_font = ImageFont.truetype(get_resource('fonts/JunicodeWL-Italic.ttf'), 50)

    def pretty_title(self):
        return u"„%s”" % self.title


class BookotekaCover(Cover):
    width = 2140
    height = 2733
    background_img = get_resource('res/cover-bookoteka.png')

    author_top = 480
    author_margin_left = 307
    author_margin_right = 233
    author_lineskip = 156
    author_color = '#d9d919'
    author_font = ImageFont.truetype(get_resource('fonts/JunicodeWL-Regular.ttf'), 130)

    title_top = 400
    title_margin_left = 307
    title_margin_right = 233
    title_lineskip = 168
    title_color = '#d9d919'
    title_font = ImageFont.truetype(get_resource('fonts/JunicodeWL-Regular.ttf'), 140)

    format = 'PNG'


class GandalfCover(Cover):
    width = 600
    height = 730
    background_img = get_resource('res/cover-gandalf.png')
    author_font = ImageFont.truetype(get_resource('fonts/JunicodeWL-Regular.ttf'), 30)
    title_font = ImageFont.truetype(get_resource('fonts/JunicodeWL-Regular.ttf'), 40)
    logo_bottom = 25
    logo_width = 250
    format = 'PNG'
