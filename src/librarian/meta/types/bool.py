from .base import MetaValue


class BoolValue(MetaValue):
    has_language = False

    @classmethod
    def from_text(cls, text):
        return cls(text == 'true')

