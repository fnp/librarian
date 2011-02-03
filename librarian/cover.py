# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import Image, ImageFont, ImageDraw, ImageFilter
from librarian import get_resource


class Cover(object):
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

    format = 'JPEG'


    exts = {
        'JPEG': 'jpg',
        'PNG': 'png',
        }

    mime_types = {
        'JPEG': 'image/jpeg',
        'PNG': 'image/png',
        }


    @staticmethod
    def draw_centered_text(text, img, font, margin_left, width, pos_y, lineskip, color, shadow_color):
        if shadow_color:
            shadow_img = Image.new('RGBA', img.size)
            shadow_draw = ImageDraw.Draw(shadow_img)
        text_img = Image.new('RGBA', img.size)
        text_draw = ImageDraw.Draw(text_img)
        while text:
            line = text
            while text_draw.textsize(line, font=font)[0] > width:
                try:
                    line, ext = line.rsplit(' ', 1)
                except:
                    break
            pos_x = margin_left + (width - text_draw.textsize(line, font=font)[0]) / 2
            if shadow_color:
                shadow_draw.text((pos_x + 3, pos_y + 3), line, font=font, fill=shadow_color)
            text_draw.text((pos_x, pos_y), line, font=font, fill=color)
            pos_y += lineskip
            text = text[len(line)+1:]
        if shadow_color:
            shadow_img = shadow_img.filter(ImageFilter.BLUR)
            img.paste(shadow_img, None, shadow_img)
        img.paste(text_img, None, text_img)
        return pos_y


    def __init__(self, author='', title=''):
        self.author = author
        self.title = title

    def pretty_author(self):
        return self.author

    def pretty_title(self):
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

        author_font = self.author_font or ImageFont.truetype(get_resource('fonts/DejaVuSerif.ttf'), 30)
        title_y = self.draw_centered_text(self.pretty_author(), img, author_font,
                    self.author_margin_left, self.width - self.author_margin_left - self.author_margin_right, self.author_top,
                    self.author_lineskip, self.author_color, self.author_shadow) + self.title_top
        title_font = self.title_font or ImageFont.truetype(get_resource('fonts/DejaVuSerif.ttf'), 40)
        self.draw_centered_text(self.pretty_title(), img, title_font,
                    self.title_margin_left, self.width - self.title_margin_left - self.title_margin_right, title_y,
                    self.title_lineskip, self.title_color, self.title_shadow)

        return img

    def mime_type(self):
        return self.mime_types[self.format]

    def ext(self):
        return self.exts[self.format]

    def save(self, *args, **kwargs):
        return self.image().save(format=self.format, *args, **kwargs)



class VirtualoCover(Cover):
    width = 600
    height = 730
    author_top = 73
    title_top = 73
    logo_bottom = 0
    logo_width = 300


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
