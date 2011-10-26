# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from __future__ import with_statement

import os
import os.path
import subprocess
from StringIO import StringIO
from copy import deepcopy
from lxml import etree
import zipfile
from tempfile import NamedTemporaryFile
from shutil import rmtree

import sys

from librarian import epub

from librarian import functions, get_resource


def transform(provider, slug=None, file_path=None, output_file=None, output_dir=None, make_dir=False, verbose=False,
              sample=None, cover=None, flags=None):
    """ produces a MOBI file

    provider: a DocProvider
    slug: slug of file to process, available by provider
    output_file: path to output file
    output_dir: path to directory to save output file to; either this or output_file must be present
    make_dir: writes output to <output_dir>/<author>/<slug>.epub instead of <output_dir>/<slug>.epub
    sample=n: generate sample e-book (with at least n paragraphs)
    cover: a cover.Cover object
    flags: less-advertising,
    """

    # if output to dir, create the file
    if output_dir is not None:
        if make_dir:
            author = unicode(book_info.author)
            output_dir = os.path.join(output_dir, author)
            try:
                os.makedirs(output_dir)
            except OSError:
                pass
        if slug:
            output_file = os.path.join(output_dir, '%s.mobi' % slug)
        else:
            output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(file_path))[0] + '.mobi')

    epub_file = NamedTemporaryFile(suffix='.epub', delete=False)
    if not flags:
        flags = []
    flags = list(flags) + ['without-fonts']
    epub.transform(provider, file_path=file_path, output_file=epub_file, verbose=verbose,
              sample=sample, cover=None, flags=flags, style=get_resource('mobi/style.css'))
    subprocess.check_call(['ebook-convert', epub_file.name, output_file])
    os.unlink(epub_file.name)
