# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import io
import urllib.parse
import urllib.request
from PIL import Image
from ..base import WLElement


class Ilustr(WLElement):
    SHOULD_HAVE_ID = True

    EPUB_TAG = HTML_TAG = 'img'

    def get_html_attr(self, builder):
        ## TODO: thumbnail.

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

        width = 1200
        if img.size[0] < width:
            th = img
        else:
            th = img.resize((width, round(width * img.size[1] / img.size[0])))

        buffer = io.BytesIO()
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

    get_epub_attr = get_html_attr
