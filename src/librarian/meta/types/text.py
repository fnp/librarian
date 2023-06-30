# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from .base import MetaValue


class TextValue(MetaValue, str):
    @classmethod
    def from_text(cls, text):
        return cls(str(text))

    def __str__(self):
        return self.value



class NameIdentifier(TextValue):
    has_language = False


class LegimiCategory(NameIdentifier):
    pass


class ThemaCategory(NameIdentifier):
    pass


class Epoch(NameIdentifier):
    pass


class Kind(NameIdentifier):
    pass


class Genre(NameIdentifier):
    pass


class Audience(NameIdentifier):
    pass
