from .txt import TxtBuilder
from .html import HtmlBuilder
from .sanitize import Sanitizer


builders = [
    TxtBuilder,
    HtmlBuilder,
    Sanitizer,
]


def get_builder_class(builder_id):
    return next(b for b in builders if b.identifier == builder_id)
