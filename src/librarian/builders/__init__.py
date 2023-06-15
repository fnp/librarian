from collections import OrderedDict
from .txt import TxtBuilder
from .html import HtmlBuilder, SnippetHtmlBuilder, StandaloneHtmlBuilder, DaisyHtmlBuilder
from .sanitize import Sanitizer
from .daisy import DaisyBuilder
from .epub import EpubBuilder
from .mobi import MobiBuilder
from .pdf import PdfBuilder


builders = OrderedDict([
    ("txt", TxtBuilder),
    ("html", HtmlBuilder),
    ("html-snippet", SnippetHtmlBuilder),
    ("html-standalone", StandaloneHtmlBuilder),
    ("html-daisy", DaisyHtmlBuilder),
    ("daisy", DaisyBuilder),
    ("sanitizer", Sanitizer),

    ("epub", EpubBuilder),
    ("mobi", MobiBuilder),
    ("pdf", PdfBuilder),
])
