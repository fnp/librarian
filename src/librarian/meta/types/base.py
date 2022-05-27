class MetaValue:
    has_language = True

    def __init__(self, value):
        self.value = value
    
    @classmethod
    def from_text(cls, text):
        raise NotImplementedError()
