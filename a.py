#!/usr/bin/env python

from librarian.document import Document as SST
from librarian.formats.pdf import PdfFormat
from librarian.utils import Context
import shutil

sst = SST.from_file('milpdf/a.xml')
of = PdfFormat(sst).build(Context(), verbose=True)
shutil.copy(of.get_filename(), 'a.pdf')



