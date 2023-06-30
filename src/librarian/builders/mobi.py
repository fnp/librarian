# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import os
import subprocess
from tempfile import NamedTemporaryFile
from librarian import functions, get_resource, OutputFile
from librarian.hyphenator import Hyphenator
from .epub import EpubBuilder


class MobiBuilder(EpubBuilder):
    file_extension = 'mobi'
    isbn_field = 'isbn_mobi'

    def build(self, document, use_kindlegen=False, converter_path=None, **kwargs):
        bibl_lng = document.meta.language
        short_lng = functions.lang_code_3to2(bibl_lng)
        try:
            self.hyphenator = Hyphenator(get_resource('res/hyph-dictionaries/hyph_' +
                                       short_lng + '.dic'))
        except:
            pass

        epub = super().build(document, **kwargs)

        devnull = open("/dev/null", 'w')
        gen_kwargs = {"stdout": devnull, "stderr": devnull}

        output_file = NamedTemporaryFile(prefix='librarian', suffix='.mobi',
                                     delete=False)
        output_file.close()

        if use_kindlegen:
            output_file_basename = os.path.basename(output_file.name)
            subprocess.check_call([converter_path or 'kindlegen',
                               '-c2', epub.get_filename(),
                               '-o', output_file_basename], **gen_kwargs)
        else:
            subprocess.check_call([converter_path or 'ebook-convert',
                               epub.get_filename(),
                               output_file.name, '--no-inline-toc',
                               '--mobi-file-type=both',
                               '--mobi-ignore-margins',
                               ], **gen_kwargs)
        devnull.close()
        return OutputFile.from_filename(output_file.name)

