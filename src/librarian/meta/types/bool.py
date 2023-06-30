# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from .base import MetaValue


class BoolValue(MetaValue):
    has_language = False

    @classmethod
    def from_text(cls, text):
        return cls(text == 'true')

