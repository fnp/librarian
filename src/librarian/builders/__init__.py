from collections import OrderedDict
from .txt import TxtBuilder
from .html import HtmlBuilder, StandaloneHtmlBuilder, DaisyHtmlBuilder
from .sanitize import Sanitizer
from .daisy import DaisyBuilder


builders = OrderedDict([
    ("txt", TxtBuilder),
    ("html", HtmlBuilder),
    ("html-standalone", StandaloneHtmlBuilder),
    ("html-daisy", DaisyHtmlBuilder),
    ("daisy", DaisyBuilder),
    ("sanitizer", Sanitizer),
])
