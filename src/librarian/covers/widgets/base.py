# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
class Widget:
    transparency = True
    margin_top = 0

    def __init__(self, cover):
        self.cover = cover
        self.setup()

    def setup(self):
        pass
        
    def build(self, w, h):
        raise NotImplementedError()

    def apply(self, img, x, y, w=None, h=None):
        my_img = self.build(w, h)
        if my_img is not None:
            img.paste(
                my_img,
                (round(x), round(y - self.margin_top)),
                my_img if self.transparency else None
            )
