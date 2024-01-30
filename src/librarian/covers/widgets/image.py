# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import PIL.Image
import PIL.ImageDraw
from librarian import get_resource
from .base import Widget


class ImageWidget(Widget):
    def build(self, w, h):
        img = PIL.Image.open(self.image_path)
        img = img.resize((round(img.size[0] / img.size[1] * h), h))
        return img
    
    
class WLLogo(ImageWidget):
    @property
    def image_path(self):
        if self.cover.color_scheme['text'] == '#fff':
            return get_resource('res/cover/logo_WL_invert.png')
        else:
            return get_resource('res/cover/logo_WL.png')


class Label(ImageWidget):
    @property
    def image_path(self):
        if self.cover.is_very_bright:
            return get_resource('res/cover/label_WLpolecaja.szary.png')
        else:
            return get_resource('res/cover/label_WLpolecaja.png')


class LogoSticker(ImageWidget):
    def __init__(self, cover, image_path):
        self.image_path = image_path

    def apply(self, img, x, y, w, h, padding_x, padding_y, radius):
        my_img = self.build(w, h, padding_x, padding_y, radius) 
        if my_img is not None:
            img.paste(
                my_img,
                (round(x), round(y - my_img.size[1])),
                my_img if self.transparency else None
            )
       

    def build(self, w, h, padding_x, padding_y, radius):
        img = PIL.Image.open(self.image_path)
        uw, uh = w - 2 * padding_x, h - 2 * padding_y
        if img.size[1] / img.size[0] > uh / uw:
            img = img.resize((round(img.size[0] / img.size[1] * uh), uh))
        else:
            img = img.resize((uw, round(img.size[1] / img.size[0] * uw)))
        sz = w, img.size[1] + 2 * padding_y
        sticker = PIL.Image.new('RGBA', sz)
        draw = PIL.ImageDraw.Draw(sticker)
        draw.rectangle((0, radius, sz[0], sz[1] - radius), (0, 0, 0))
        draw.rectangle((radius, 0, sz[0] - radius, sz[1]), (0, 0, 0))
        draw.ellipse((0, 0, 2 * radius, 2 * radius), (0, 0, 0))
        draw.ellipse((0, sz[1] - 2 * radius, 2 * radius, sz[1]), (0, 0, 0))
        draw.ellipse((sz[0] - 2 * radius, 0, sz[0], 2 * radius), (0, 0, 0))
        draw.ellipse((sz[0] - 2 * radius, sz[1] - 2 * radius, sz[0], sz[1]), (0, 0, 0))
        sticker.paste(
            img,
            (
                round(padding_x + (uw - img.size[0]) / 2), padding_y),
            img
        )
        return sticker
