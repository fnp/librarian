from copy import copy
from ..base import WLElement


class Mat(WLElement):
    def html_build(self, builder):
        e = copy(self)
        e.tag = 'math'
        e.attrib['xmlns'] = 'http://www.w3.org/1998/Math/MathML'
        builder.cursor.append(e)
