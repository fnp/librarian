# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from copy import deepcopy
import os
import subprocess
from tempfile import NamedTemporaryFile

from librarian import OutputFile
from librarian.cover import DefaultEbookCover
from librarian import get_resource


def transform(wldoc, verbose=False, sample=None, cover=None, 
              use_kindlegen=False, flags=None):
    """ produces a MOBI file

    wldoc: a WLDocument
    sample=n: generate sample e-book (with at least n paragraphs)
    cover: a cover.Cover factory overriding default
    flags: less-advertising,
    """

    document = deepcopy(wldoc)
    del wldoc
    book_info = document.book_info

    if not flags:
        flags = []
    flags = list(flags)
    
    epub = document.as_epub(verbose=verbose, sample=sample,
                            html_toc=True, cover=True, flags=flags)
    if verbose:
        kwargs = {}
    else:
        devnull = open("/dev/null", 'w')
        kwargs = {"stdout": devnull, "stderr": devnull}

    output_file = NamedTemporaryFile(prefix='librarian', suffix='.mobi', delete=False)
    output_file.close()

    if use_kindlegen:
        output_file_basename = os.path.basename(output_file.name)
        subprocess.check_call(
            ['kindlegen', '-c2', epub.get_filename(), '-o', output_file_basename],
            **kwargs
        )
    else:
        subprocess.check_call(
            ['ebook-convert', epub.get_filename(), output_file.name,
            '--no-inline-toc', 
            '--mobi-file-type=both', 
            '--mobi-ignore-margins'], **kwargs
        )
    return OutputFile.from_filename(output_file.name)
