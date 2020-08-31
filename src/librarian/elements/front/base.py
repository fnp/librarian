from ..base import WLElement


class HeaderElement(WLElement):
    HTML_TAG = 'span'
    
    def txt_build(self, builder):
        builder.enter_fragment('header')
        super(HeaderElement, self).txt_build(builder)
        builder.exit_fragment()

    def html_build(self, builder):
        builder.enter_fragment('header')
        super(HeaderElement, self).html_build(builder)
        builder.exit_fragment()
