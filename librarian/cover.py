# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import Image, ImageFont, ImageDraw, ImageFilter
from librarian import get_resource


def cover(author, title,
          width, height, background_color, background_img,
          author_top, author_margin_left, author_margin_right, author_lineskip, author_color, author_font, author_shadow,
          title_top, title_margin_left, title_margin_right, title_lineskip, title_color, title_font, title_shadow,
          logo_width, logo_bottom
          ):
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


    img = Image.new('RGB', (width, height), background_color)

    if background_img:
        background = Image.open(background_img)
        img.paste(background)
        del background

    # WL logo
    if logo_width:
        logo = Image.open(get_resource('res/wl-logo.png'))
        logo = logo.resize((logo_width, logo.size[1] * logo_width / logo.size[0]))
        img.paste(logo, ((width - logo_width) / 2, img.size[1] - logo.size[1] - logo_bottom))

    title_y = draw_centered_text(author, img, author_font,
                    author_margin_left, width - author_margin_left - author_margin_right, author_top,
                    author_lineskip, author_color, author_shadow) + title_top
    draw_centered_text(title, img, title_font,
                    title_margin_left, width - title_margin_left - title_margin_right, title_y,
                    title_lineskip, title_color, title_shadow)

    return img


def virtualo_cover(author, title):
    return cover(author, title,
          600, 730, '#fff', None,
          73, 20, 20, 40, '#000', ImageFont.truetype(get_resource('fonts/DejaVuSerif.ttf'), 30), None,
          73, 20, 20, 54, '#000', ImageFont.truetype(get_resource('fonts/DejaVuSerif.ttf'), 40), None,
          300, 0
          )

def asbis_cover(author, title):
    return cover(author, u"„%s”" % title,
          800, 800, '#000', '',
          455, 230, 170, 60, '#fff', ImageFont.truetype(get_resource('fonts/JunicodeWL-Italic.ttf'), 50), '#000',
          0, 230, 170, 60, '#fff', ImageFont.truetype(get_resource('fonts/JunicodeWL-Italic.ttf'), 50), '#000',
          None, None
          )

