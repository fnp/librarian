from .base import MetaValue


class TextValue(MetaValue, str):
    @classmethod
    def from_text(cls, text):
        return cls(str(text))

    def __str__(self):
        return self.value
