import PIL.Image
from librarian.cover import Cover, Metric
from .utils.color import algo_contrast_or_hue, luminance, is_very_bright
from .utils.textbox import DoesNotFit
from .widgets.author import AuthorBox
from .widgets.background import Background
from .widgets.image import WLLogo, Label
from .widgets.marquise import Marquise
from .widgets.title import TitleBox


class MarquiseCover(Cover):
    additional_logos = []
    square_variant = False

    width = 2100
    height = 2970
    margin = 100
    logo_h = 177
    author_width = 1300

    title_box_top = 262

    color_schemes = [
        {
            'rgb': (0xc3, 0x27, 0x21),
            'text': '#000',
        },
        {
            'rgb': (0xa0, 0xbf, 0x38),
            'text': '#000',
        },
        {
            'rgb': (0xed, 0xc0, 0x16),
            'text': '#000',
        },
        {
            'rgb': (0x47, 0x66, 0x75),
            'text': '#fff',
        }
    ]
    for c in color_schemes:
        c['luminance'] = luminance(c['rgb'])
        cim = PIL.Image.new('RGB', (1, 1))
        cim.putpixel((0, 0), c['rgb'])
        cim.convert('HSV')
        c['hsv'] = cim.getpixel((0, 0))

    
    def set_size(self, final_width, final_height):
        if final_width is None:
            self.m = Metric(self, 1)
        else:
            if final_width > self.width:
                self.m = Metric(self, final_width / self.width)
            else:
                self.m = Metric(self, 1)
                self.scale_after = final_width / self.width
            
        if final_height is not None:
            self.height = round(final_height / self.scale_after / self.m._scale)

        self.square_variant = self.height / self.width < 250 / 210

        marquise_square_small = int(self.width / 2) - 300
        marquise_square_big = int(self.width / 2) - 100
        marquise_a4_small = 2970 - self.width
        marquise_a4_big = marquise_a4_small + 100
        
        self.marquise_small = int(round(marquise_square_small + (marquise_a4_small - marquise_square_small) * (self.height - self.width) / (2970 - 2100)))
        self.marquise_big = int(round(marquise_square_big + (marquise_a4_big - marquise_square_big) * (self.height - self.width) / (2970 - 2100)))
        self.marquise_xl = self.marquise_big + 200

        if self.marquise_small > self.marquise_big:
            self.marquise_small = self.marquise_big

    def set_color_scheme_from(self, img):
        self.color_scheme = algo_contrast_or_hue(img, self.color_schemes)
        self.is_very_bright = is_very_bright(img)

    def image(self):
        img = PIL.Image.new('RGB', (self.m.width, self.m.height), self.background_color)
        
        bg = Background(self)

        if self.square_variant:
            layout_options = [
                (self.m.marquise_small, 1),
                (self.m.marquise_big, 2),
                (self.m.marquise_big, 3),
                (self.m.marquise_big, None),
            ]
        else:
            layout_options = [
                (self.m.marquise_small, 2),
                (self.m.marquise_small, 1),
                (self.m.marquise_big, 3),
                (self.m.marquise_xl, 4),
                (self.m.marquise_xl, None),
            ]

        # Trying all the layout options with decreasing scale.
        title_box = None
        title_scale = 1
        while title_box is None:
            for marquise_h, lines in layout_options:
                title_box_height = marquise_h - self.m.title_box_top - self.m.margin
                try:
                    title_box = TitleBox(
                        self,
                        self.m.width - 2 * self.m.margin,
                        title_box_height,
                        lines,
                        scale=title_scale
                    )
                except DoesNotFit:
                    continue
                else:
                    break
            title_scale *= .99

        self.marquise_height = marquise_h
        marquise = Marquise(self, marquise_h)

        bg.apply(
            img,
            0, marquise.edge_top,
            self.m.width, self.m.height - marquise.edge_top
        )
        self.set_color_scheme_from(
            img.crop((
                0, marquise.edge_top,
                self.m.width, marquise.edge_top + (
                    self.m.height - marquise.edge_top
                ) / 4
            ))
        )

        marquise.apply(
            img, 0, 0, self.m.width
        )
        title_box.apply(
            img,
            marquise.title_box_position[0],
            marquise.title_box_position[1],
        )

        AuthorBox(self, self.m.author_width).apply(
            img, self.m.width - self.m.margin - self.m.author_width, self.m.margin
        )
        WLLogo(self).apply(img, self.m.margin, self.m.margin, None, self.m.logo_h)

                              
        for logo in self.additional_logos:
            LogoSticker(self, logo).apply(img, 0, 0)


        return img


    
class LabelMarquiseCover(MarquiseCover):
    label_left = 95
    label_top = 105
    label_w = 710
    label_h = 710
    
    def image(self):
        img = super().image()

        Label(self).apply(
            img,
            self.m.label_left,
            self.marquise_height - self.m.label_top,
            self.m.label_w,
            self.m.label_h
        )

        return img
