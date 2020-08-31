from .wers import Wers


class WersWciety(Wers):
    @property
    def typ(self):
        ## Temporary legacy compatibility fix.
        return 2 if 'typ' in self.attrib else 1

        v = self.attrib.get('typ')
        return int(v) if v else 1

    def _txt_build_inner(self, builder):
        builder.push_text('  ' * self.typ, prepared=True)
        super(WersWciety, self)._txt_build_inner(builder)

