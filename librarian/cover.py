# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import re
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from StringIO import StringIO
from librarian import get_resource, IOFile


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
        try:
            self.author = ", ".join(auth.readable() for auth in book_info.authors)
        except AttributeError:
            self.author = ""
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
        return IOFile.from_string(imgstr.getvalue())

    def for_pdf(self):
        return IOFile.from_filename(get_resource('pdf/cover_image.sty'), {
            'cover.png': self.output_file(),
        })
