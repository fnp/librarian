# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import os
import subprocess
from tempfile import NamedTemporaryFile

from librarian import OutputFile
from librarian.cover import WLCover
from librarian import get_resource


def transform(wldoc, verbose=False,
              sample=None, cover=None, flags=None):
    """ produces a MOBI file

    wldoc: a WLDocument
    sample=n: generate sample e-book (with at least n paragraphs)
    cover: a cover.Cover object
    flags: less-advertising,
    """

    book_info = wldoc.book_info

    # provide a cover by default
    if not cover:
        cover = WLCover
    cover_file = NamedTemporaryFile(suffix='.png', delete=False)
    c = cover(book_info.author.readable(), book_info.title)
    c.save(cover_file)

    if not flags:
        flags = []
    flags = list(flags) + ['without-fonts']
    epub = wldoc.as_epub(verbose=verbose, sample=sample, html_toc=True,
            flags=flags, style=get_resource('mobi/style.css'))

    if verbose:
        kwargs = {}
    else:
        devnull = open("/dev/null", 'w')
        kwargs = {"stdout": devnull, "stderr": devnull}

    output_file = NamedTemporaryFile(prefix='librarian', suffix='.mobi', delete=False)
    output_file.close()
    subprocess.check_call(['ebook-convert', epub.get_filename(), output_file.name,
            '--no-inline-toc', '--cover=%s' % cover_file.name], **kwargs)
    os.unlink(cover_file.name)
    return OutputFile.from_filename(output_file.name)