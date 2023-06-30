# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
class MetaValue:
    has_language = True

    def __init__(self, value):
        self.value = value
    
    @classmethod
    def from_text(cls, text):
        raise NotImplementedError()
