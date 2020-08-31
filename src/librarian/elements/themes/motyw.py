from ..base import WLElement


class Motyw(WLElement):
    def txt_build(self, builder):
        pass


    def feed_to(self, builder):
        assert not len(self)
        themes = [
            normalize_text(t.strip()) for t in self.text.split(',')
        ]
        builder.set_themes(self.attrib['id'], themes)
