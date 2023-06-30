# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class End(WLElement):
    HTML_TAG = 'span'

    def get_html_attr(self, builder):
        fid = self.attrib.get('id', '')[1:]
        return {
            "class": "theme-end",
            "fid": fid
        }
