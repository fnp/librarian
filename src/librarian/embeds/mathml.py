# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from lxml import etree
from librarian import get_resource
from . import TreeEmbed, create_embed, downgrades_to


class MathML(TreeEmbed):
    @downgrades_to('application/x-latex')
    def to_latex(self):
        """
        >>> print(MathML(etree.fromstring(
        ...     '<mat>a &lt; b</mat>'
        ... )).to_latex().data.strip())
        a < b

        >>> print(MathML(etree.fromstring(
        ...     '<mat>&lt; &amp; &amp;lt; &#65;</mat>'
        ... )).to_latex().data.strip())
        < & &lt; A

        """
        xslt = etree.parse(get_resource('res/embeds/mathml/mathml2latex.xslt'))
        output = self.tree.xslt(xslt)
        text = str(output)
        # Workaround for entities being preserved in output.
        # But there should be a better way.
        text = text.replace('&lt;', '<').replace('&amp;', '&')
        return create_embed('application/x-latex', data=text)
