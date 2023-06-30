# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import PIL.Image
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

