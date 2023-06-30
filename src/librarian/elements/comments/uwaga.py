# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class Uwaga(WLElement):
    def txt_build(self, builder):
        pass

    def html_build(self, builder):
        pass

    def epub_build(self, builder):
        pass

    def validate(self):
        return
