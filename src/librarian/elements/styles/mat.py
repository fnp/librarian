# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from copy import copy
from ..base import WLElement


class Mat(WLElement):
    def html_build(self, builder):
        e = copy(self)
        e.tag = 'math'
        e.attrib['xmlns'] = 'http://www.w3.org/1998/Math/MathML'
        builder.cursor.append(e)

    def epub_build(self, builder):
        builder.start_element('img', {"src": builder.mathml(self)})
        builder.end_element()
