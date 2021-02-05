# -*- coding: utf-8
from __future__ import unicode_literals

from ..base import WLElement


class Footnote(WLElement):
    def txt_build(self, builder):
        pass

    def html_build(self, builder):
        if not builder.with_footnotes:
            return

        builder.footnote_counter += 1
        fn_no = builder.footnote_counter
        footnote_id = 'footnote-idm{}'.format(self.attrib['_compat_ordered_id'])
        anchor_id = 'anchor-idm{}'.format(self.attrib['_compat_ordered_id'])

        # Add anchor.
        builder.start_element(
            'a',
            {
                "href": '#{}'.format(footnote_id),
                "class": "annotation-anchor",
                "id": anchor_id,
            }
        )
        builder.push_text('[{}]'.format(fn_no))
        builder.end_element()
        
        # Add actual footnote.
        builder.enter_fragment('footnotes')
        builder.start_element('div', {'class': 'fn-{}'.format(self.tag)})
        builder.push_text('\n') # Compat
        builder.start_element('a', {'name': footnote_id})
        builder.end_element()
        builder.start_element('a', {
            'href': '#{}'.format(anchor_id), 'class': 'annotation'
        })
        builder.push_text('[{}]'.format(fn_no))
        builder.end_element()

        builder.start_element('p')
        super(Footnote, self).html_build(builder)

        builder.push_text(' [{}]'.format(self.qualifier))
        builder.end_element()
        builder.end_element()
        builder.exit_fragment()


class PA(Footnote):
    """Przypis autorski."""
    @property
    def qualifier(self):
        _ = self.gettext
        return _("author's footnote")


class PT(Footnote):
    """Przypis tłumacza."""
    @property
    def qualifier(self):
        _ = self.gettext
        return _("translator's footnote")


class PR(Footnote):
    """Przypis redakcyjny."""
    @property
    def qualifier(self):
        _ = self.gettext
        return _("editor's footnote")


class PE(Footnote):
    """Przypis redakcji źródła."""
    @property
    def qualifier(self):
        _ = self.gettext
        return _("source editor's footnote")
