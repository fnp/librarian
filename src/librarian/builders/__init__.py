from collections import OrderedDict
from .txt import TxtBuilder
from .html import HtmlBuilder, StandaloneHtmlBuilder
from .sanitize import Sanitizer


builders = OrderedDict([
    ("txt", TxtBuilder),
    ("html", HtmlBuilder),
    ("html-standalone", StandaloneHtmlBuilder),
    ("sanitizer", Sanitizer),
])
