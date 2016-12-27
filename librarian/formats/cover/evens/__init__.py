# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import urllib
from urllib2 import urlopen, URLError

from librarian import DCNS, BuildError
from .. import Cover


class EvensCover(Cover):
    format_name = u"Evens cover image"
    width = 1024
    height = 1365
    author_top = 900
    title_top = 30
    logo_bottom = 100

    def set_images(self, ctx):
        try:
            cover_url = self.doc.meta.get(DCNS('relation.coverimage.url'))[0]
        except IndexError:
            raise BuildError('No cover specified (metadata field relation.coverimage.url missing)')
        if not cover_url:
            raise BuildError('No cover specified (metadata field relation.coverimage.url empty)')
        if cover_url.startswith('file://'):
            cover_url = ctx.files_path + urllib.quote(cover_url[7:])
        try:
            self.background_img = urlopen(cover_url)
        except URLError:
            raise BuildError('Cannot open the cover image: %s' % cover_url)

        if getattr(ctx, 'cover_logo', None):
            self.logo_width = 150
            self.logo_file = urlopen(ctx.cover_logo)
