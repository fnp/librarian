import io
import time
from urllib.request import urlopen
import PIL.Image
from .base import Widget


class Background(Widget):
    transparency = False

    def __init__(self, cover, crop_to_square=True):
        self.crop_to_square = crop_to_square
        super().__init__(cover)

    def setup(self):
        self.img = None
        if self.cover.book_info.cover_url:
            while True:
                try:
                    data = io.BytesIO(urlopen(self.cover.book_info.cover_url, timeout=3).read())
                except:
                    time.sleep(2)
                else:
                    break
                
            img = PIL.Image.open(data)

            if self.crop_to_square:
                # crop top square.
                if img.size[1] > img.size[0]:
                    img = img.crop((0, 0, img.size[0], img.size[0]))
                else:
                    left = round((img.size[0] - img.size[1])/2)
                    img = img.crop((
                        left,
                        0,
                        left + img.size[1],
                        img.size[1]
                    ))
            self.img = img

    def build(self, w, h):
        if not self.img:
            return
        img = self.img
        scale = max(
            w / img.size[0],
            h / img.size[1]
        )
        img = self.img.resize((
            round(scale * img.size[0]),
            round(scale * img.size[1]),
        ))
        img = img.crop((
            int((img.size[0] - w) / 2),
            0,
            w + int((img.size[0] - w) / 2),
            h))
        
        return img
