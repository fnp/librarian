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

    
class Epoch(NameIdentifier):
    pass


class Kind(NameIdentifier):
    pass


class Genre(NameIdentifier):
    pass


class Audience(NameIdentifier):
    pass
