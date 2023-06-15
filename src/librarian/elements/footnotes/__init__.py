# -*- coding: utf-8
from __future__ import unicode_literals

from ..base import WLElement


class Footnote(WLElement):
    NO_TOC = True
    START_INLINE = True
    ASIDE = True

    def signal(self, signal):
        if signal == 'INLINE':
            self.START_INLINE = False
        else:
            super().signal(signal)
    
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

    def epub_build(self, builder):
        fn_no = builder.assign_footnote_number()
        part_number = getattr(
            builder,
            'chunk_counter',
            1
        )

        builder.start_element(
            'a',
            {
                'class': 'anchor',
                'id': f'anchor-{fn_no}',
                'href': f'annotations.xhtml#annotation-{fn_no}',
            }
        )
        builder.start_element('sup', {})
        builder.push_text(str(fn_no))
        builder.end_element()
        builder.end_element()

        
        builder.enter_fragment('footnotes')
        builder.start_element('div', {
            'id': f'annotation-{fn_no}',
            'class': "annotation"
        })
        builder.start_element('a', {
            'href': f"part{part_number}.xhtml#anchor-{fn_no}"
        })
        builder.push_text(str(fn_no))
        builder.end_element()
        builder.push_text('. ')

        super().epub_build(builder)
        builder.push_text(' [' + self.qualifier + ']')
        builder.end_element()

        builder.push_text('\n')

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
