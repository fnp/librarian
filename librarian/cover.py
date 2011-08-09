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

    author_align = 'c'
    author_top = 100
    author_margin_left = 20
    author_margin_right = 20
    author_lineskip = 40
    author_color = '#000'
    author_shadow = None
    author_font = None
    author_wrap = True

    title_align = 'c'
    title_top = 100
    title_margin_left = 20
    title_margin_right = 20
    title_lineskip = 54
    title_color = '#000'
    title_shadow = None
    title_font = None
    title_wrap = True

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
    def person_shortener(text):
        yield text
        chunks = text.split()
        n_chunks = len(chunks)
        # make initials from given names, starting from last
        for i in range(n_chunks - 2, -1, -1):
            chunks[i] = chunks[i][0] + '.'
            yield " ".join(chunks)
        # remove given names initials, starting from last
        while len(chunks) > 2:
            del chunks[1]
            yield " ".join(chunks)

    @staticmethod
    def title_shortener(text):
        yield text
        chunks = text.split()
        n_chunks = len(chunks)
        # remove words, starting from last one
        while len(chunks) > 1:
            del chunks[-1]
            yield " ".join(chunks) + u'…'

    @staticmethod
    def draw_text(text, img, font, align, shortener, margin_left, width, pos_y, lineskip, color, shadow_color):
        if shadow_color:
            shadow_img = Image.new('RGBA', img.size)
            shadow_draw = ImageDraw.Draw(shadow_img)
        text_img = Image.new('RGBA', img.size)
        text_draw = ImageDraw.Draw(text_img)
        while text:
            if shortener:
                for line in shortener(text):
                    if text_draw.textsize(line, font=font)[0] <= width:
                        break
                text = ''
            else:
                line = text
                while text_draw.textsize(line, font=font)[0] > width:
                    try:
                        line, ext = line.rsplit(' ', 1)
                    except:
                        break
                text = text[len(line)+1:]
            pos_x = margin_left
            if align == 'c':
                pos_x += (width - text_draw.textsize(line, font=font)[0]) / 2
            elif align == 'r':
                pos_x += (width - text_draw.textsize(line, font=font)[0])
            if shadow_color:
                shadow_draw.text((pos_x + 3, pos_y + 3), line, font=font, fill=shadow_color)
            text_draw.text((pos_x, pos_y), line, font=font, fill=color)
            pos_y += lineskip
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
            try:
                img.paste(background, None, background)
            except ValueError, e:
                img.paste(background)
            del background

        # WL logo
        if self.logo_width:
            logo = Image.open(get_resource('res/wl-logo.png'))
            logo = logo.resize((self.logo_width, logo.size[1] * self.logo_width / logo.size[0]))
            img.paste(logo, ((self.width - self.logo_width) / 2, img.size[1] - logo.size[1] - self.logo_bottom))

        author_font = self.author_font or ImageFont.truetype(get_resource('fonts/DejaVuSerif.ttf'), 30)
        author_shortener = None if self.author_wrap else self.person_shortener 
        title_y = self.draw_text(self.pretty_author(), img, author_font, self.author_align, author_shortener,
                    self.author_margin_left, self.width - self.author_margin_left - self.author_margin_right, self.author_top,
                    self.author_lineskip, self.author_color, self.author_shadow) + self.title_top
        title_shortener = None if self.title_wrap else self.title_shortener 
        title_font = self.title_font or ImageFont.truetype(get_resource('fonts/DejaVuSerif.ttf'), 40)
        self.draw_text(self.pretty_title(), img, title_font, self.title_align, title_shortener,
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


class ArtaTechCover(Cover):
    width = 600
    height = 800
    background_img = get_resource('res/cover-arta-tech.jpg')
    author_top = 132
    author_margin_left = 235
    author_margin_right = 23
    author_align = 'r'
    author_font = ImageFont.truetype(get_resource('fonts/DroidSans.ttf'), 32)
    author_color = '#555555'
    author_wrap = False
    title_top = 17
    title_margin_right = 21
    title_margin_left = 60
    title_align = 'r'
    title_font = ImageFont.truetype(get_resource('fonts/EBGaramond-Regular.ttf'), 42)
    title_color = '#222222'
    title_wrap = False
    format = 'JPEG'

    def pretty_author(self):
        return self.author.upper()


def ImageCover(img):
    """ a class factory for simple image covers """
    img = Image.open(img)

    class ImgCover(Cover):
        def image(self):
            return img

        @property
        def format(self):
            return self.image().format

    return ImgCover
