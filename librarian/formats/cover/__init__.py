# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import re
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from StringIO import StringIO
from librarian import DCNS, BuildError
from librarian.output import OutputFile
from librarian.utils import get_resource
from librarian.formats import Format


class Metric(object):
    """Gets metrics from an object, scaling it by a factor."""
    def __init__(self, obj, scale):
        self._obj = obj
        self._scale = float(scale)

    def __getattr__(self, name):
        src = getattr(self._obj, name)
        if src and self._scale:
            src = type(src)(self._scale * src)
        return src


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


class Cover(Format):
    """Base class for cover images generator."""
    format_name = u"cover image"

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
    author_font_ttf = get_resource('fonts/DejaVuSerif.ttf')
    author_font_size = 30

    title_top = 100
    title_margin_left = 20
    title_margin_right = 20
    title_lineskip = 54
    title_color = '#000'
    title_shadow = None
    title_font_ttf = get_resource('fonts/DejaVuSerif.ttf')
    title_font_size = 40

    logo_bottom = None
    logo_width = None
    logo_file = get_resource('res/wl-logo.png')
    uses_dc_cover = False

    format = 'JPEG'
    scale = 1

    exts = {
        'JPEG': 'jpg',
        'PNG': 'png',
        }

    mime_types = {
        'JPEG': 'image/jpeg',
        'PNG': 'image/png',
        }

    def __init__(self, doc, format=None, width=None, height=None):
        super(Cover, self).__init__(doc)
        self.author = ", ".join(auth for auth in doc.meta.get(DCNS('creator')))
        self.title = doc.meta.title()
        if format is not None:
            self.format = format
        scale = max(float(width or 0) / self.width, float(height or 0) / self.height)
        if scale:
            self.scale = scale

    def pretty_author(self):
        """Allows for decorating author's name."""
        return self.author

    def pretty_title(self):
        """Allows for decorating title."""
        return self.title

    def image(self):
        metr = Metric(self, self.scale)
        img = Image.new('RGB', (metr.width, metr.height), self.background_color)

        if self.background_img:
            background = Image.open(self.background_img)
            resized = background.resize((1024, background.height*1024/background.width), Image.ANTIALIAS)
            resized = resized.convert('RGBA')
            img.paste(resized, (0, 0), resized)
            del background, resized

        if metr.logo_width:
            logo = Image.open(self.logo_file)
            logo = logo.resize((metr.logo_width, logo.size[1] * metr.logo_width / logo.size[0]), Image.ANTIALIAS)
            logo = logo.convert('RGBA')
            img.paste(logo, ((metr.width - metr.logo_width) / 2,
                             img.size[1] - logo.size[1] - metr.logo_bottom), logo)

        top = metr.author_top
        tbox = TextBox(
            metr.width - metr.author_margin_left - metr.author_margin_right,
            metr.height - top,
            )
            
        author_font = ImageFont.truetype(
            self.author_font_ttf, metr.author_font_size)
        tbox.text(
            self.pretty_author(), self.author_color, author_font,
            metr.author_lineskip, self.author_shadow)
        text_img = tbox.image()
        img.paste(text_img, (metr.author_margin_left, top), text_img)

        top += text_img.size[1] + metr.title_top
        tbox = TextBox(
            metr.width - metr.title_margin_left - metr.title_margin_right,
            metr.height - top,
            )
        title_font = ImageFont.truetype(
            self.title_font_ttf, metr.title_font_size)
        tbox.text(
            self.pretty_title(), self.title_color, title_font,
            metr.title_lineskip, self.title_shadow)
        text_img = tbox.image()
        img.paste(text_img, (metr.title_margin_left, top), text_img)

        return img
        # imgstr = StringIO()
        # img.save(imgstr, format=self.format, quality=95)
        # OutputFile.from_stringing(imgstr.getvalue())

    def mime_type(self):
        return self.mime_types[self.format]

    @property
    def format_ext(self):
        return self.exts[self.format]

    def save(self, *args, **kwargs):
        return self.image().save(format=self.format, quality=95, *args, **kwargs)

    def build(self, *args, **kwargs):
        imgstr = StringIO()
        self.save(imgstr, *args, **kwargs)
        return OutputFile.from_string(imgstr.getvalue())
