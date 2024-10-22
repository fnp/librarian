# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from collections import OrderedDict
from .txt import TxtBuilder
from .html import HtmlBuilder, SnippetHtmlBuilder, StandaloneHtmlBuilder, DaisyHtmlBuilder
from .sanitize import Sanitizer
from .daisy import DaisyBuilder
from .epub import EpubBuilder
from .mobi import MobiBuilder
from .pdf import PdfBuilder
from .fb2 import FB2Builder


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
    ("fb2", FB2Builder),
])
