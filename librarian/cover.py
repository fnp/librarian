# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import re
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from StringIO import StringIO
from librarian import get_resource, OutputFile, URLOpener


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
    uses_dc_cover = False

    format = 'JPEG'
    scale = 1
    scale_after = 1

    exts = {
        'JPEG': 'jpg',
        'PNG': 'png',
        }

    mime_types = {
        'JPEG': 'image/jpeg',
        'PNG': 'image/png',
        }

    def __init__(self, book_info, format=None, width=None, height=None):
        self.author = ", ".join(auth.readable() for auth in book_info.authors)
        self.title = book_info.title
        if format is not None:
            self.format = format
        if width and height:
            self.height = height * self.width / width
        scale = max(float(width or 0) / self.width, float(height or 0) / self.height)
        if scale >= 1:
            self.scale = scale
        elif scale:
            self.scale_after = scale

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
            img.paste(background, None, background)
            del background

        # WL logo
        if metr.logo_width:
            logo = Image.open(get_resource('res/wl-logo.png'))
            logo = logo.resize((metr.logo_width, logo.size[1] * metr.logo_width / logo.size[0]))
            img.paste(logo, ((metr.width - metr.logo_width) / 2, img.size[1] - logo.size[1] - metr.logo_bottom))

        top = metr.author_top
        tbox = TextBox(
            metr.width - metr.author_margin_left - metr.author_margin_right,
            metr.height - top,
            )
            
        author_font = ImageFont.truetype(
            self.author_font_ttf, metr.author_font_size)
        tbox.text(self.pretty_author(), self.author_color, author_font, metr.author_lineskip, self.author_shadow)
        text_img = tbox.image()
        img.paste(text_img, (metr.author_margin_left, top), text_img)

        top += text_img.size[1] + metr.title_top
        tbox = TextBox(
            metr.width - metr.title_margin_left - metr.title_margin_right,
            metr.height - top,
            )
        title_font = ImageFont.truetype(
            self.title_font_ttf, metr.title_font_size)
        tbox.text(self.pretty_title(), self.title_color, title_font, metr.title_lineskip, self.title_shadow)
        text_img = tbox.image()
        img.paste(text_img, (metr.title_margin_left, top), text_img)

        return img

    def final_image(self):
        img = self.image()
        if self.scale_after != 1:
            img = img.resize((
                    int(round(img.size[0] * self.scale_after)),
                    int(round(img.size[1] * self.scale_after))),
                Image.ANTIALIAS)
        return img

    def mime_type(self):
        return self.mime_types[self.format]

    def ext(self):
        return self.exts[self.format]

    def save(self, *args, **kwargs):
        default_kwargs = {
                'format': self.format,
                'quality': 95,
        }
        default_kwargs.update(kwargs)
        return self.final_image().save(*args, **default_kwargs)

    def output_file(self, *args, **kwargs):
        imgstr = StringIO()
        self.save(imgstr, *args, **kwargs)
        return OutputFile.from_string(imgstr.getvalue())


class WLCover(Cover):
    """Wolne Lektury cover without logos."""
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
    bar_color = '#000'
    box_position = 'middle'
    background_color = '#444'
    author_color = '#444'
    background_img = get_resource('res/cover.png')
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

    kind_box_position = {
        u'Liryka': 'top',
        u'Epika': 'bottom',
    }

    def __init__(self, book_info, format=None, width=None, height=None):
        super(WLCover, self).__init__(book_info, format=format, width=width, height=height)
        # Set box position.
        self.box_position = book_info.cover_box_position or \
            self.kind_box_position.get(book_info.kind, self.box_position)
        # Set bar color.
        if book_info.cover_bar_color == 'none':
            self.bar_width = 0
        else:
            self.bar_color = book_info.cover_bar_color or \
                self.epoch_colors.get(book_info.epoch, self.bar_color)
        # Set title color.
        self.title_color = self.epoch_colors.get(book_info.epoch, self.title_color)

        if book_info.cover_url:
            url = book_info.cover_url
            bg_src = None
            if bg_src is None:
                bg_src = URLOpener().open(url)
            self.background_img = StringIO(bg_src.read())
            bg_src.close()

    def pretty_author(self):
        return self.author.upper()

    def add_box(self, img):
        if self.box_position == 'none':
            return img

        metr = Metric(self, self.scale)

        # Write author name.
        box = TextBox(metr.title_box_width, metr.height, padding_y=metr.box_padding_y)
        author_font = ImageFont.truetype(
            self.author_font_ttf, metr.author_font_size)
        box.text(self.pretty_author(),
                 font=author_font,
                 line_height=metr.author_lineskip,
                 color=self.author_color,
                 shadow_color=self.author_shadow)

        box.skip(metr.box_above_line)
        box.draw.line((metr.box_line_left, box.height, metr.box_line_right, box.height),
                      fill=self.author_color, width=metr.box_line_width)
        box.skip(metr.box_below_line)

        # Write title.
        title_font = ImageFont.truetype(
            self.title_font_ttf, metr.title_font_size)
        box.text(self.pretty_title(),
                 line_height=metr.title_lineskip,
                 font=title_font,
                 color=self.title_color,
                 shadow_color=self.title_shadow)

        box_img = box.image()

        # Find box position.
        if self.box_position == 'top':
            box_top = metr.box_top_margin
        elif self.box_position == 'bottom':
            box_top = metr.height - metr.box_bottom_margin - box_img.size[1]
        else:   # Middle.
            box_top = (metr.height - box_img.size[1]) / 2

        box_left = metr.bar_width + (metr.width - metr.bar_width - box_img.size[0]) / 2

        # Draw the white box.
        ImageDraw.Draw(img).rectangle(
            (box_left, box_top, box_left + box_img.size[0], box_top + box_img.size[1]), fill='#fff')
        # Paste the contents into the white box.
        img.paste(box_img, (box_left, box_top), box_img)
        return img

    def image(self):
        metr = Metric(self, self.scale)
        img = Image.new('RGB', (metr.width, metr.height), self.background_color)
        draw = ImageDraw.Draw(img)

        draw.rectangle((0, 0, metr.bar_width, metr.height), fill=self.bar_color)

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

        img = self.add_box(img)

        return img


class LogoWLCover(WLCover):
    gradient_height = 90
    gradient_logo_height = 60
    gradient_logo_margin_right = 30
    gradient_logo_spacing = 40
    gradient_color = '#000'
    gradient_opacity = .6
    gradient_logos = [
        'res/wl-logo-white.png',
        'res/fnp-logo-white.png',
    ]

    def image(self):
        img = super(LogoWLCover, self).image()
        metr = Metric(self, self.scale)
        gradient = Image.new('RGBA', (metr.width - metr.bar_width, metr.gradient_height), self.gradient_color)
        gradient_mask = Image.new('L', (metr.width - metr.bar_width, metr.gradient_height))
        draw = ImageDraw.Draw(gradient_mask)
        for line in range(0, metr.gradient_height):
            draw.line(
                (0, line, metr.width - metr.bar_width, line),
                fill=int(255 * self.gradient_opacity * line / metr.gradient_height))
        img.paste(gradient, (metr.bar_width, metr.height - metr.gradient_height), mask=gradient_mask)

        cursor = metr.width - metr.gradient_logo_margin_right
        logo_top = metr.height - metr.gradient_height / 2 - metr.gradient_logo_height / 2
        for logo_path in self.gradient_logos[::-1]:
            logo = Image.open(get_resource(logo_path))
            logo = logo.resize(
                (logo.size[0] * metr.gradient_logo_height / logo.size[1], metr.gradient_logo_height),
                Image.ANTIALIAS)
            cursor -= logo.size[0]
            img.paste(logo, (cursor, logo_top), mask=logo)
            cursor -= metr.gradient_logo_spacing

        return img


class EbookpointCover(LogoWLCover):
    gradient_logo_height = 58
    gradient_logo_spacing = 25
    gradient_logos = [
        'res/ebookpoint-logo-white.png',
        'res/wl-logo-white.png',
        'res/fnp-logo-white.png',
    ]


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
    author_font_ttf = get_resource('fonts/JunicodeWL-Italic.ttf')
    author_font_size = 50

    title_top = 0
    title_margin_left = 118
    title_margin_right = 62
    title_lineskip = 60
    title_color = '#fff'
    title_shadow = '#000'
    title_font_ttf = get_resource('fonts/JunicodeWL-Italic.ttf')
    title_font_size = 50

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
    author_font_ttf = get_resource('fonts/JunicodeWL-Regular.ttf')
    author_font_size = 130

    title_top = 400
    title_margin_left = 307
    title_margin_right = 233
    title_lineskip = 168
    title_color = '#d9d919'
    title_font_ttf = get_resource('fonts/JunicodeWL-Regular.ttf')
    title_font_size = 140

    format = 'PNG'


class GandalfCover(Cover):
    width = 600
    height = 730
    background_img = get_resource('res/cover-gandalf.png')
    author_font_ttf = get_resource('fonts/JunicodeWL-Regular.ttf')
    author_font_size = 30
    title_font_ttf = get_resource('fonts/JunicodeWL-Regular.ttf')
    title_font_size = 40
    logo_bottom = 25
    logo_width = 250
    format = 'PNG'


DefaultEbookCover = LogoWLCover
