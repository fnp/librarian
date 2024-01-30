# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import re
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from io import BytesIO
from librarian import get_resource, OutputFile, URLOpener


class Metric:
    """Gets metrics from an object, scaling it by a factor."""
    def __init__(self, obj, scale):
        self._obj = obj
        self._scale = float(scale)

    def __getattr__(self, name):
        src = getattr(self._obj, name)
        if src and self._scale:
            return type(src)(self._scale * src)
        else:
            return src


class TextBox:
    """Creates an Image with a series of centered strings."""

    SHADOW_X = 3
    SHADOW_Y = 3
    SHADOW_BLUR = 3

    def __init__(self, max_width, max_height, padding_x=None, padding_y=None, bar_width=0, bar_color=None):
        if padding_x is None:
            padding_x = self.SHADOW_X + self.SHADOW_BLUR
        if padding_y is None:
            padding_y = self.SHADOW_Y + self.SHADOW_BLUR

        self.max_width = max_width
        self.bar_width = bar_width
        self.bar_color = bar_color
        self.max_text_width = max_width - 2 * padding_x - bar_width
        self.padding_x = padding_x
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
             shadow_color=None, centering=True):
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

                if len(line) > 2 and line[-2] == ' ':
                    line = line[:-2]

                line_width = self.draw.textsize(line, font=font)[0]
            line = line.strip() + ' '

            if centering:
                pos_x = (self.max_width - line_width) // 2
            else:
                pos_x = self.bar_width + self.padding_x

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
                                   int(round(self.height + self.padding_y))))

        if self.shadow_img:
            shadow = self.shadow_img.filter(ImageFilter.BLUR)
            image.paste(shadow, (0, 0), shadow)
            image.paste(self.img, (0, 0), self.img)
        else:
            image.paste(self.img, (0, 0))
        return image


class Cover:
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

    def __init__(self, book_info, format=None, width=None, height=None, cover_logo=None):
        self.book_info = book_info

        self.predesigned = False
        if book_info.cover_class == 'image':
            self.predesigned = True

        # TODO: deprecated
        if book_info.cover_box_position == 'none':
            self.predesigned = True

        self.authors = [auth.readable() for auth in book_info.authors]
        self.title = book_info.title
        if format is not None:
            self.format = format
        self.set_size(width, height)
        self.cover_logo = cover_logo

    def set_size(self, width, height):
        if width and height:
            self.height = int(round(height * self.width / width))
        scale = max(float(width or 0) / self.width,
                    float(height or 0) / self.height)
        if scale >= 1:
            self.scale = scale
        elif scale:
            self.scale_after = scale

    def pretty_authors(self):
        """Allows for decorating authors' names."""
        return self.authors

    def pretty_title(self):
        """Allows for decorating title."""
        return self.title

    def image(self):
        metr = Metric(self, self.scale)
        img = Image.new('RGB', (metr.width, metr.height),
                        self.background_color)

        if self.background_img:
            background = Image.open(self.background_img)
            img.paste(background, None, background)
            del background

        # WL logo
        if metr.logo_width:
            logo = Image.open(get_resource('res/wl-logo.png'))
            logo = logo.resize((
                metr.logo_width,
                int(round(logo.size[1] * metr.logo_width / logo.size[0]))
            ))
            img.paste(logo, (
                (metr.width - metr.logo_width) // 2,
                img.size[1] - logo.size[1] - metr.logo_bottom
            ))

        top = metr.author_top
        tbox = TextBox(
            metr.width - metr.author_margin_left - metr.author_margin_right,
            metr.height - top,
            )

        author_font = ImageFont.truetype(
            self.author_font_ttf, metr.author_font_size,
            layout_engine=ImageFont.Layout.BASIC)
        for pa in self.pretty_authors():
            tbox.text(pa, self.author_color, author_font, metr.author_lineskip,
                      self.author_shadow)
        text_img = tbox.image()
        img.paste(text_img, (metr.author_margin_left, top), text_img)

        top += text_img.size[1] + metr.title_top
        tbox = TextBox(
            metr.width - metr.title_margin_left - metr.title_margin_right,
            metr.height - top,
            )
        title_font = ImageFont.truetype(
            self.title_font_ttf, metr.title_font_size,
            layout_engine=ImageFont.Layout.BASIC)
        tbox.text(self.pretty_title(), self.title_color, title_font,
                  metr.title_lineskip, self.title_shadow)
        text_img = tbox.image()
        img.paste(text_img, (metr.title_margin_left, top), text_img)

        return img

    def final_image(self):
        img = self.image()
        if self.scale_after != 1:
            img = img.resize((
                    int(round(img.size[0] * self.scale_after)),
                    int(round(img.size[1] * self.scale_after))),
                Image.Resampling.LANCZOS)
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
        imgstr = BytesIO()
        self.save(imgstr, *args, **kwargs)
        return OutputFile.from_bytes(imgstr.getvalue())


class WLCover(Cover):
    """Wolne Lektury cover without logos."""
    width = 600
    height = 833
    uses_dc_cover = True
    author_font_ttf = get_resource('fonts/JunicodeWL-Regular.ttf')
    author_font_size = 20
    author_lineskip = 30
    author_centering = True
    title_font_ttf = get_resource('fonts/DejaVuSerif-Bold.ttf')
    title_font_size = 30
    title_lineskip = 40
    title_box_width = 350
    title_centering = True

    box_top_margin = 100
    box_bottom_margin = 100
    box_padding_y = 20
    box_above_line = 10
    box_below_line = 15
    box_line_left = 75
    box_line_right = 275
    box_line_width = 2
    box_padding_x = 0
    box_bar_width = 0

    logo_top = 15
    logo_width = 140

    bar_width = 35
    bar_color = '#000'
    box_position = 'middle'
    background_color = '#444'
    author_color = '#444'
    background_img = get_resource('res/cover.png')
    background_top = False
    format = 'JPEG'

    epoch_colors = {
        'Starożytność': '#9e3610',
        'Średniowiecze': '#564c09',
        'Renesans': '#8ca629',
        'Barok': '#a6820a',
        'Oświecenie': '#f2802e',
        'Romantyzm': '#db4b16',
        'Pozytywizm': '#961060',
        'Modernizm': '#7784e0',
        'Dwudziestolecie międzywojenne': '#3044cf',
        'Współczesność': '#06393d',
    }
    set_title_color = True

    kind_box_position = {
        'Liryka': 'top',
        'Epika': 'bottom',
    }

    def __init__(self, book_info, format=None, width=None, height=None,
                 bleed=0, cover_logo=None):
        super(WLCover, self).__init__(book_info, format=format, width=width,
                                      height=height)

        self.slug = book_info.url.slug
        # Set box position.
        self.box_position = book_info.cover_box_position or \
            self.kind_box_position.get(book_info.kind, self.box_position)
        # Set bar color.
        if book_info.cover_bar_color == 'none':
            self.bar_width = 0
        else:
            self.bar_color = book_info.cover_bar_color or \
                self.get_variable_color(book_info) or self.bar_color
        # Set title color.
        if self.set_title_color:
            self.title_color = self.get_variable_color(book_info) or self.title_color

        self.bleed = bleed
        self.box_top_margin += bleed
        self.box_bottom_margin += bleed
        self.bar_width += bleed

        if book_info.cover_url:
            url = book_info.cover_url
            bg_src = None
            while True:
                try:
                    if bg_src is None:
                        import requests
                        bg_src = requests.get(url, timeout=5)
                    self.background_img = BytesIO(bg_src.content)
                    bg_src.close()
                except Exception as e:
                    bg_src = None
                    print(e)
                    import time
                    time.sleep(1)
                else:
                    break

    def get_variable_color(self, book_info):
        return self.epoch_colors.get(book_info.epoch, None)

    def pretty_authors(self):
        return [a.upper() for a in self.authors]

    def add_box(self, img):
        if self.box_position == 'none':
            return img

        metr = Metric(self, self.scale)

        # Write author name.
        box = TextBox(metr.title_box_width - 2 * self.bleed, metr.height,
                      padding_y=metr.box_padding_y,
                      padding_x=metr.box_padding_x,
                      bar_width=metr.box_bar_width,
                      bar_color=self.bar_color,
                      )
        author_font = ImageFont.truetype(
            self.author_font_ttf, metr.author_font_size,
            layout_engine=ImageFont.Layout.BASIC)
        for pa in self.pretty_authors():
            box.text(pa, font=author_font, line_height=metr.author_lineskip,
                     color=self.author_color, shadow_color=self.author_shadow,
                     centering=self.author_centering
                     )

        box.skip(metr.box_above_line)
        box.draw.line(
            (metr.box_line_left, box.height, metr.box_line_right, box.height),
            fill=self.author_color, width=metr.box_line_width
        )
        box.skip(metr.box_below_line)

        # Write title.
        title_font = ImageFont.truetype(
            self.title_font_ttf, metr.title_font_size,
            layout_engine=ImageFont.Layout.BASIC)
        box.text(self.pretty_title(),
                 line_height=metr.title_lineskip,
                 font=title_font,
                 color=self.title_color,
                 shadow_color=self.title_shadow,
                 centering=self.title_centering
                 )

        box_img = box.image()

        # Find box position.
        if self.box_position == 'bottom' or box_img.size[1] + metr.box_top_margin + metr.box_bottom_margin > metr.height:
            box_top = metr.height - metr.box_bottom_margin - box_img.size[1]
        elif self.box_position == 'top':
            box_top = metr.box_top_margin
        else:   # Middle.
            box_top = (metr.height - box_img.size[1]) // 2

        box_left = metr.bar_width + (
            metr.width - metr.bar_width - box_img.size[0] - self.bleed
        ) // 2

        # Draw the white box.
        img_draw = ImageDraw.Draw(img)
        img_draw.rectangle(
            (
                box_left,
                box_top,
                box_left + box_img.size[0],
                box_top + box_img.size[1]
            ),
            fill='#fff'
        )
        # Paste the contents into the white box.
        img.paste(box_img, (box_left, box_top), box_img)
        if self.box_bar_width:
            img_draw.rectangle(
                (
                    box_left,
                    box_top,
                    box_left + metr.box_bar_width,
                    box_top + box_img.size[1]
                ),
                fill=self.bar_color
            )
        return img

    def add_cut_lines(self, img):
        line_ratio = 0.5
        if self.bleed == 0:
            return img
        metr = Metric(self, self.scale)
        draw = ImageDraw.Draw(img)
        for corner_x, corner_y in (
                (0, 0), (metr.width, 0),
                (0, metr.height), (metr.width, metr.height)
                ):
            dir_x = 1 if corner_x == 0 else -1
            dir_y = 1 if corner_y == 0 else -1
            for offset in (-1, 0, 1):
                draw.line(
                    (
                        corner_x,
                        corner_y + dir_y * metr.bleed + offset,
                        corner_x + dir_x * metr.bleed * line_ratio,
                        corner_y + dir_y * metr.bleed + offset
                    ),
                    fill='black' if offset == 0 else 'white',
                    width=1
                )
                draw.line(
                    (
                        corner_x + dir_x * metr.bleed + offset,
                        corner_y,
                        corner_x + dir_x * metr.bleed + offset,
                        corner_y + dir_y * metr.bleed * line_ratio
                    ),
                    fill='black' if offset == 0 else 'white',
                    width=1
                )
        return img

    def image(self):
        metr = Metric(self, self.scale)
        img = Image.new('RGB', (metr.width, metr.height),
                        self.background_color)
        draw = ImageDraw.Draw(img)

        draw.rectangle((0, 0, metr.bar_width, metr.height),
                       fill=self.bar_color)

        if self.background_img:
            src = Image.open(self.background_img)
            trg_size = (metr.width - metr.bar_width, metr.height)
            if src.size[0] * trg_size[1] < src.size[1] * trg_size[0]:
                resized = (
                    trg_size[0],
                    int(round(src.size[1] * trg_size[0] / src.size[0]))
                )
                if self.background_top:
                    cut = 0
                else:
                    cut = (resized[1] - trg_size[1]) // 2
                src = src.resize(resized, Image.Resampling.LANCZOS)
                src = src.crop((0, cut, src.size[0], src.size[1] - cut))
            else:
                resized = (
                    int(round(src.size[0] * trg_size[1] / src.size[1])),
                    trg_size[1],
                )
                cut = (resized[0] - trg_size[0]) // 2
                src = src.resize(resized, Image.Resampling.LANCZOS)
                src = src.crop((cut, 0, src.size[0] - cut, src.size[1]))

            img.paste(src, (metr.bar_width, 0))
            del src

        img = self.add_box(img)

        # img = self.add_cut_lines(img)

        return img


class WLNoBoxCover(WLCover):
    def add_box(self, img):
        return img


class LogoWLCover(WLCover):
    gradient_height = 90
    gradient_easing = 90
    gradient_logo_height = 57
    gradient_logo_max_width = 200
    gradient_logo_margin_right = 30
    gradient_logo_spacing = 40
    gradient_color = '#000'
    gradient_opacity = .6
    gradient_logos = [
        'res/wl-logo-white.png',
        'res/fnp-logo-white.png',
    ]
    annotation = None
    annotation_height = 10

    logos_right = True
    gradient_logo_centering = False

    qrcode = None


    def __init__(self, book_info, *args, cover_logo=None, **kwargs):
        super(LogoWLCover, self).__init__(book_info, *args, **kwargs)
        self.gradient_height += self.bleed
        self.gradient_logo_margin_right += self.bleed

        self.additional_cover_logos = [
            BytesIO(URLOpener().open(cover_logo_url).read())
            for cover_logo_url in book_info.cover_logo_urls
        ]
        self.end_cover_logos = []
        if cover_logo:
            self.additional_cover_logos.append(
                    open(cover_logo, 'rb')
                    )

    @property
    def has_gradient_logos(self):
        return self.gradient_logos or self.additional_cover_logos or self.end_cover_logos or self.annotation or self.qrcode is not None

    def add_gradient_logos(self, img, metr):
        gradient = Image.new(
            'RGBA',
            (metr.width - metr.bar_width, metr.gradient_height),
            self.gradient_color
        )
        gradient_mask = Image.new(
            'L',
            (metr.width - metr.bar_width, metr.gradient_height)
        )
        draw = ImageDraw.Draw(gradient_mask)
        for line in range(0, metr.gradient_easing):
            draw.line(
                (0, line, metr.width - metr.bar_width, line),
                fill=int(
                    255 * self.gradient_opacity * line / metr.gradient_easing
                )
            )
        draw.rectangle((
            0, metr.gradient_easing,
            metr.width - metr.bar_width, metr.gradient_height
        ), fill=int(255 * self.gradient_opacity))
            
            
        img.paste(gradient,
                  (metr.bar_width, metr.height - metr.gradient_height),
                  mask=gradient_mask)

        if self.logos_right:
            cursor = metr.width - metr.gradient_logo_margin_right
        else:
            cursor = metr.gradient_logo_margin_right
        logo_top = int(
            metr.height
            - metr.gradient_height / 2
            - metr.gradient_logo_height / 2 - metr.bleed
        )

        logos = [
            get_resource(logo_path)
            for logo_path in self.gradient_logos
        ]

        logos = self.additional_cover_logos + logos + self.end_cover_logos

        logos = [
            Image.open(logo_bytes).convert('RGBA')
            for logo_bytes in logos
        ]

        if self.qrcode is not None:
            import qrcode
            logos.append(qrcode.make(f'https://wolnelektury.pl/katalog/lektura/{self.slug}/?{self.qrcode}'))

        if self.logos_right:
            logos.reverse()

        # See if logos fit into the gradient. If not, scale down accordingly.
        space_for_logos = (
            metr.width
            - metr.bar_width
            - 2 * metr.gradient_logo_margin_right + self.bleed
        )
        widths = [
            min(
                metr.gradient_logo_max_width,
                logo.size[0] * metr.gradient_logo_height / logo.size[1]
            )
            for logo in logos]
        taken_space = sum(widths) + (len(logos) - 1) * metr.gradient_logo_spacing
        if taken_space > space_for_logos:
            logo_scale = space_for_logos / taken_space
        else:
            logo_scale = 1
            if self.gradient_logo_centering:
                cursor += int((space_for_logos - taken_space) / 2)
        logo_scale = (
            space_for_logos / taken_space
            if taken_space > space_for_logos else 1
        )
        #logo_top += int(metr.gradient_logo_height * (1 - logo_scale) / 2)

        for i, logo in enumerate(logos):
            if i == -1:
                L_scale = 1
            else:
                L_scale = logo_scale
            L_top = logo_top + int(metr.gradient_logo_height * (1 - L_scale) / 2)

            logo = logo.resize(
                (
                    int(round(widths[i] * L_scale)),
                    int(round(
                        logo.size[1] * widths[i] / logo.size[0] * L_scale
                    ))
                ),
                Image.Resampling.LANCZOS)
            if self.logos_right:
                cursor -= logo.size[0]

            img.paste(
                logo,
                (
                    cursor,
                    L_top
                    #int(round(logo_top + (metr.gradient_logo_height - logo.size[1]) * L_scale / 2))
                ),
                mask=logo
            )
            if self.logos_right:
                cursor -= int(round(metr.gradient_logo_spacing * logo_scale))
            else:
                cursor += int(round(metr.gradient_logo_spacing * logo_scale)) + logo.size[0]

        if self.annotation:
            img2 = Image.new('RGBA', (metr.height, metr.height), color=None)
            draw = ImageDraw.Draw(img2)
            author_font = ImageFont.truetype(
                self.author_font_ttf, metr.annotation_height,
                layout_engine=ImageFont.Layout.BASIC)
            draw.text((self.annotation_height, self.annotation_height), self.annotation, font=author_font, fill='#FFFFFF')
            img2.show()
            img2 = img2.rotate(90)
            img2.show()
            img.putalpha(0)
            img.alpha_composite(img2, (0, 0))
            img = img.convert('RGB')

        return img
    
    def image(self):
        img = super(LogoWLCover, self).image()
        metr = Metric(self, self.scale)
        if self.has_gradient_logos:
            img = self.add_gradient_logos(img, metr)
        return img


class LegimiCover(LogoWLCover):
    width = 210
    height = 297
    bar_width = 0
    # Other bar

    author_font_ttf = get_resource('fonts/Lora-Regular.ttf')
    author_font_size = 15
    author_lineskip = 19.5
    author_centering = False
    title_font_ttf = get_resource('fonts/Lora-Bold.ttf')
    title_font_size = 15
    title_lineskip = 19.5
    title_centering = False
    
    title_box_width = 210

    box_bottom_margin = 20
    box_padding_x = 20
    box_padding_y = 10   # do baseline
    box_above_line = 6
    box_below_line = 0
    box_line_left = 0
    box_line_right = 0

    box_line_width = 0

    box_bar_width = 20

    #logo_top = 15
    #logo_width = 140

    bar_color = '#000'
    box_position = 'bottom'
    background_color = '#444'
    author_color = '#000'
    title_color = '#000'
    set_title_color = False

    kind_box_position = {}

    box_bottom_margin_logos_add = 10
    gradient_height = 30
    gradient_easing = 0
    gradient_logo_height = 20
    gradient_logo_max_width = 200
    gradient_logo_margin_right = 10
    gradient_logo_spacing = 20
    gradient_color = '#000'
    gradient_opacity = .5
    gradient_logos = [
        'res/wl-logo-white.png',
    ]
    logos_right = False
    gradient_logo_centering = True
    background_top = True

    genre_colors = {
        'Artykuł': '#bf001a',
        'Artykuł naukowy': '#bf001a',
        'Dziennik': '#bf001a',
        'Esej': '#bf001a',
        'Felieton': '#bf001a',
        'Kronika': '#bf001a',
        'List': '#bf001a',
        'Manifest': '#bf001a',
        'Odczyt': '#bf001a',
        'Pamiętnik': '#bf001a',
        'Poradnik': '#bf001a',
        'Praca naukowa': '#bf001a',
        'Publicystyka': '#bf001a',
        'Reportaż': '#bf001a',
        'Reportaż podróżniczy': '#bf001a',
        'Rozprawa': '#bf001a',
        'Rozprawa polityczna': '#bf001a',
        'Traktat': '#bf001a',
    }
    kind_colors = {
        'Epika': '#9bbb2b',
        'Liryka': '#3e626f',
        'Dramat': '#ecbe00',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.has_gradient_logos:
            self.box_bottom_margin += self.box_bottom_margin_logos_add

    def pretty_authors(self):
        return self.authors

    def get_variable_color(self, book_info):
        for genre in book_info.genres:
            if genre in self.genre_colors:
                return self.genre_colors[genre]
        for kind in book_info.kinds:
            if kind in self.kind_colors:
                return self.kind_colors[kind]

class LegimiCornerCover(LegimiCover):
    gradient_logos = []
    corner_width = 120
    corner_image = get_resource('res/book-band.png')
    
    def image(self):
        image = super().image()
        metr = Metric(self, self.scale)

        if self.corner_image:
            corner = Image.open(self.corner_image).convert('RGBA')
            corner = corner.resize(
                (
                    int(round(metr.corner_width)),
                    int(round(corner.size[1] / corner.size[0] * metr.corner_width))
                )
            )
            image.paste(corner, (
                metr.width - int(round(metr.corner_width)),
                0,
            ), corner)
        return image

class LegimiAudiobookCover(LegimiCornerCover):
    corner_width = 82.5
    corner_image = get_resource('res/audiobook-sticker.png')
    height = 210


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
        return "„%s”" % self.title


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


class KMLUCover(LogoWLCover):
    gradient_logo_height = 58
    gradient_logo_spacing = 25
    gradient_logos = [
        'res/kmlu-logo-white.png',
        'res/wl-logo-white.png',
        'res/fnp-logo-white.png',
    ]


class MPWCover(LogoWLCover):
    gradient_logo_height = 57
    gradient_logo_spacing = 25
    gradient_logos = [
        'res/mpw-logo-white.png',
        'res/wl-logo-white.png',
        'res/fnp-logo-white.png',
    ]


class AtriumCover(LogoWLCover):
    gradient_logo_height = 58
    gradient_logo_spacing = 25
    gradient_logos = [
        'res/atrium-logo.png',
        'res/wl-logo-white.png',
        'res/fnp-logo-white.png',
    ]


class BNCover(LogoWLCover):
    gradient_logos = [
        'res/dofinansowano.png',
        'res/MKIDN.jpg',
        'res/BN.png',
        'res/wl-logo-white.png',
    ]
#    annotation = 'Zadanie „Udostępnienie publikacji w formatach cyfrowych” w ramach Narodowego Programu Rozwoju Czytelnictwa. Dofinansowano ze środków Ministra Kultury, Dziedzictwa Narodowego i Sportu.'


class FactoryCover(LogoWLCover):
    gradient_logos = [
        'res/factory.jpg',
        'res/wl-logo-white.png',
    ]
    qrcode = 'pk_campaign=factory22'
    format = 'PNG'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('bleed', 10)
        return super().__init__(*args, **kwargs)

    def ext(self):
        return 'pdf'

    def output_file(self, *args, **kwargs):
        imgfile = super().output_file(*args, **kwargs)
        import subprocess
        import tempfile
        with tempfile.TemporaryDirectory(prefix='factory-', dir='.') as d:
            import os
            import shutil
            with open(d + '/cover.png', 'wb') as f:
                f.write(imgfile.get_bytes())
            shutil.copy(get_resource('res/factory-cover.svg'), d)
            subprocess.call(['inkscape', f'--export-filename={d}/cover.pdf', d + '/factory-cover.svg'])
            with open(d + '/cover.pdf', 'rb') as f:
                return OutputFile.from_bytes(f.read())



from librarian.covers.marquise import MarquiseCover, LabelMarquiseCover

COVER_CLASSES = {
    'legacy': LogoWLCover,
    'kmlu': KMLUCover,
    'mpw': MPWCover,
    'atrium': AtriumCover,
    'bn': BNCover,
    'legimi': LegimiCover,
    'legimi-corner': LegimiCornerCover,
    'legimi-audiobook': LegimiAudiobookCover,
    'factory': FactoryCover,
    'm': MarquiseCover,
    'm-label': LabelMarquiseCover,
    'default': MarquiseCover,
}


def make_cover(book_info, *args, **kwargs):
    cover_class_name = None
    if 'cover_class' in kwargs:
        cover_class_name = kwargs.pop('cover_class')
    if not cover_class_name:
        cover_class_name = 'default'
    cover_class = COVER_CLASSES[cover_class_name]
    return cover_class(book_info, *args, **kwargs)
