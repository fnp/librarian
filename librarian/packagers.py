# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import os
from librarian import pdf, epub, mobi, DirDocProvider, ParseError
from librarian.parser import WLDocument

from util import makedirs


class Packager(object):
    cover = None
    flags = None

    @classmethod
    def transform(cls, *args, **kwargs):
        return cls.converter.transform(*args, **kwargs)

    @classmethod
    def prepare_file(cls, main_input, output_dir, verbose=False, overwrite=False):
        path, fname = os.path.realpath(main_input).rsplit('/', 1)
        provider = DirDocProvider(path)
        slug, ext = os.path.splitext(fname)

        if output_dir != '':
            makedirs(output_dir)
        outfile = os.path.join(output_dir, slug + '.' + cls.ext)
        if os.path.exists(outfile) and not overwrite:
            return

        doc = WLDocument.from_file(main_input, provider=provider)
        output_file = cls.transform(doc, cover=cls.cover, flags=cls.flags)
        doc.save_output_file(output_file, output_path=outfile)

    @classmethod
    def prepare(cls, input_filenames, output_dir='', verbose=False, overwrite=False):
        try:
            for main_input in input_filenames:
                if verbose:
                    print main_input
                cls.prepare_file(main_input, output_dir, verbose, overwrite)
        except ParseError, e:
            print '%(file)s:%(name)s:%(message)s' % {
                'file': main_input,
                'name': e.__class__.__name__,
                'message': e.message
            }


class EpubPackager(Packager):
    converter = epub
    ext = 'epub'


class MobiPackager(Packager):
    converter = mobi
    ext = 'mobi'


class PdfPackager(Packager):
    converter = pdf
    ext = 'pdf'

    @classmethod
    def transform(cls, *args, **kwargs):
        return cls.converter.transform(*args, morefloats='new', **kwargs)
