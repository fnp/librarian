# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from copy import copy
from ..base import WLElement


class Mat(WLElement):
    STRIP = True

    def html_build(self, builder):
        e = copy(self)
        e.tag = 'math'
        e.attrib['xmlns'] = 'http://www.w3.org/1998/Math/MathML'
        builder.cursor.append(e)

    def epub_build(self, builder):
        builder.start_element('img', {"src": builder.mathml(self)})
        builder.end_element()


class M(WLElement):
    STRIP = True


class MRow(M):
    pass


class MFenced(M):
    TXT_PREFIX = '('
    TXT_SUFFIX = ')'


class MFrac(M):
    TXT_PREFIX = '('
    TXT_SUFFIX = ')'

    def txt_after_child(self, builder, child_count):
        if child_count:
            builder.push_text(') / (')


class MSup(M):
    def txt_after_child(self, builder, child_count):
        if child_count:
            builder.push_text(' ^ ')
