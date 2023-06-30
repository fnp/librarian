# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from librarian import OutputFile


class PdfBuilder:
    # Obowiązkowe
    file_extension = 'pdf'
    def build(self, document, mp3):
        # stub
        return OutputFile.from_bytes(b'')



