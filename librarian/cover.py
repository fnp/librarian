# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import Image, ImageFont, ImageDraw
from librarian import get_resource


def cover(width, height, author, title):
    def draw_centered_text(text, draw, font, width, pos_y, lineskip):
        while text:
            line = text
            while draw.textsize(line, font=font)[0] > width:
                try:
                    line, ext = line.rsplit(' ', 1)
                except:
                    break
            draw.text(((img.size[0] - draw.textsize(line, font=font)[0]) / 2, pos_y), line, font=font, fill='#000')
            pos_y += lineskip
            text = text[len(line)+1:]
        return pos_y


    img = Image.new('RGB', (width, height), (255, 255, 255))

    # WL logo
    logo = Image.open(get_resource('pdf/wl-logo.png'))
    logo = logo.resize((img.size[0] / 2, logo.size[1] * img.size[0] / 2 / logo.size[0]))
    img.paste(logo, (width / 4, img.size[1] - logo.size[1]))

    draw = ImageDraw.Draw(img)
    author_font = ImageFont.truetype(get_resource('fonts/DejaVuSerif.ttf'), width/20)
    title_y = draw_centered_text(author, draw, author_font, width*9/10, height/10, width/15) + height/10

    title_font = ImageFont.truetype(get_resource('fonts/DejaVuSerif.ttf'), width/15)
    draw_centered_text(title, draw, title_font, width*9/10, title_y, width/11)

    return img
