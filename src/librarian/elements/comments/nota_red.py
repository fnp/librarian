from ..base import WLElement


class NotaRed(WLElement):
    def txt_build(self, builder):
        pass

    def html_build(self, builder):
        builder.enter_fragment('nota_red')
        super(NotaRed, self).html_build(builder)
        builder.exit_fragment()

    def epub_build(self, builder):
        pass
