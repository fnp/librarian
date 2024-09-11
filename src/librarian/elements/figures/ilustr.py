# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import io
import urllib.parse
import urllib.request
from PIL import Image
from ..base import WLElement


MAX_PNG_WEIGHT = 200000


class Ilustr(WLElement):
    NUMBERING = 'i'

    EPUB_TAG = HTML_TAG = 'img'

    def get_html_attr(self, builder):
        cls = 'ilustr'
        if self.attrib.get('wyrownanie'):
            cls += ' ' + self.attrib['wyrownanie']
        if self.attrib.get('oblew'):
            cls += ' oblew'
        attr = {
            'class': cls,
            'alt': self.attrib.get('alt', ''),
            'title': self.attrib.get('alt', ''),
            'src': self.attrib.get('src', ''),
            }
        if self.attrib.get('srcset'):
            attr['srcset'] = self.attrib['srcset']
            attr['sizes'] = '''
            (min-width: 718px) 600px,
            (min-width: 600px) calc(100vw - 118px),
            (min-width: 320px) calc(100vw - 75px),
            (min-width: 15em) calc(100wv - 60px),
            calc(100wv - 40px)
            '''
        if self.attrib.get('szer'):
            attr['style'] = 'width: ' + self.attrib['szer']
        return attr

    def get_epub_attr(self, builder):
        url = urllib.parse.urljoin(
            builder.base_url,
            self.get('src')
        )
        
        imgfile = urllib.request.urlopen(url)
        img = Image.open(imgfile)
        th_format, ext, media_type = {
            'GIF': ('GIF', 'gif', 'image/gif'),
            'PNG': ('PNG', 'png', 'image/png'),
        }.get(img.format, ('JPEG', 'jpg', 'image/jpeg'))

        width = 600
        if img.size[0] < width:
            th = img
        else:
            th = img.resize((width, round(width * img.size[1] / img.size[0])))

        buffer = io.BytesIO()
        th.save(buffer, format=th_format)

        # Limit PNG to 200K. If larger, convert to JPEG.
        if th_format == 'PNG' and buffer.tell() > MAX_PNG_WEIGHT:
            th_format, ext, media_type = 'JPEG', 'jpg', 'image/jpeg'
            if th.mode != 'RGB':
                buffer = io.BytesIO()
                th = Image.alpha_composite(
                    Image.new('RGBA', th.size, '#fff'),
                    th.convert('RGBA')
                )
                th = th.convert('RGB')
            th.save(buffer, format=th_format)

        imgfile.close()
        file_name = 'image%d.%s' % (
            builder.assign_image_number(),
            ext
        )

        builder.add_file(
            content=buffer.getvalue(),
            file_name=file_name,
            media_type=media_type,
        )
        
        return {
            'src': file_name,
            'alt': self.attrib.get('alt', ''),
            'title': self.attrib.get('alt', ''),
        }
