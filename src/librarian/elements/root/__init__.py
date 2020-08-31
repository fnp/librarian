from ..base import WLElement
from ..masters import Master


class Utwor(WLElement):
    CAN_HAVE_TEXT = False

    @property
    def meta(self):
        if self.meta_object is not None:
            return self.meta_object
        else:
            # Deprecated: allow RDF record in master.
            for c in self:
                if isinstance(c, Master) and c.meta_object is not None:
                    return c.meta_object
            # This should not generally happen.
            if self.getparent() is not None:
                return self.getparent().meta
