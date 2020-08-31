from ..base import WLElement


class SekcjaAsterysk(WLElement):
    TXT_TOP_MARGIN = 2
    TXT_BOTTOM_MARGIN = 4
    TXT_LEGACY_TOP_MARGIN = 2
    TXT_LEGACY_BOTTOM_MARGIN = 2

    def _txt_build_inner(self, builder):
        builder.push_text('*')
