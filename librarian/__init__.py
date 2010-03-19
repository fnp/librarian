# -*- coding: utf-8 -*-
# exception classes

class ParseError(Exception):
    pass

class ValidationError(Exception):
    pass

class NoDublinCore(ValidationError):
    pass
