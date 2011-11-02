# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import os
import os.path
import subprocess
from tempfile import NamedTemporaryFile
from lxml import etree

from librarian.cover import WLCover
from librarian import epub, get_resource, NoDublinCore, RDFNS
from librarian.dcparser import BookInfo


def transform(provider, slug=None, file_path=None, output_file=None, output_dir=None, make_dir=False, verbose=False,
              sample=None, cover=None, flags=None):
    """ produces a MOBI file

    provider: a DocProvider
    slug: slug of file to process, available by provider
    output_file: path to output file
    output_dir: path to directory to save output file to; either this or output_file must be present
    make_dir: writes output to <output_dir>/<author>/<slug>.mobi instead of <output_dir>/<slug>.mobi
    sample=n: generate sample e-book (with at least n paragraphs)
    cover: a cover.Cover object
    flags: less-advertising,
    """

    # read metadata from the first file
    if file_path:
        if slug:
            raise ValueError('slug or file_path should be specified, not both')
        f = open(file_path, 'r')
        input_xml = etree.parse(f)
        f.close()
    else:
        if not slug:
            raise ValueError('either slug or file_path should be specified')
        input_xml = etree.parse(provider[slug])

    metadata = input_xml.find('.//'+RDFNS('Description'))
    if metadata is None:
        raise NoDublinCore('Document has no DublinCore - which is required.')
    book_info = BookInfo.from_element(input_xml)

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

    # provide a cover by default
    if not cover:
        cover = WLCover
    cover_file = NamedTemporaryFile(suffix='.png', delete=False)
    c = cover(book_info.author.readable(), book_info.title)
    c.save(cover_file)

    epub_file = NamedTemporaryFile(suffix='.epub', delete=False)
    if not flags:
        flags = []
    flags = list(flags) + ['without-fonts']
    epub.transform(provider, file_path=file_path, output_file=epub_file, verbose=verbose,
              sample=sample, html_toc=True, flags=flags, style=get_resource('mobi/style.css'))

    if verbose:
        kwargs = {}
    else:
        devnull = open("/dev/null", 'w')
        kwargs = {"stdout": devnull, "stderr": devnull}
    subprocess.check_call(['ebook-convert', epub_file.name, output_file,
            '--no-inline-toc', '--cover=%s' % cover_file.name], **kwargs)
    os.unlink(epub_file.name)
    os.unlink(cover_file.name)
