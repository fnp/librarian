# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
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
        # Fallback
        return self.document.base_meta

    @property
    def master(self):
        for c in self:
            if isinstance(c, Master):
                return c
