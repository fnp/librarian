# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import ImageFont
from librarian import get_resource
from librarian.cover import Cover


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
