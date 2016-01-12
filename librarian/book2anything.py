#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import os.path
import optparse

from librarian import DirDocProvider, ParseError
from librarian.parser import WLDocument
from librarian.cover import DefaultEbookCover


class Option(object):
    """Option for optparse. Use it like `optparse.OptionParser.add_option`."""
    def __init__(self, *names, **options):
        self.names = names
        self.options = options

    def add(self, parser):
        parser.add_option(*self.names, **self.options)

    def name(self):
        return self.options['dest']

    def value(self, options):
        return getattr(options, self.name())


class Book2Anything(object):
    """A class for creating book2... scripts.
    
    Subclass it for any format you want to convert to.
    """
    format_name = None  # Set format name, like "PDF".
    ext = None  # Set file extension, like "pdf".
    uses_cover = False  # Can it add a cover?
    cover_optional = True  # Only relevant if uses_cover
    uses_provider = False  # Does it need a DocProvider?
    transform = None  # Transform method. Uses WLDocument.as_{ext} by default.
    parser_options = []  # List of Option objects for additional parser args.
    transform_options = []  # List of Option objects for additional transform args.
    transform_flags = []  # List of Option objects for supported transform flags.

    @classmethod
    def run(cls):
        # Parse commandline arguments
        usage = """Usage: %%prog [options] SOURCE [SOURCE...]
        Convert SOURCE files to %s format.""" % cls.format_name

        parser = optparse.OptionParser(usage=usage)

        parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False,
                          help='print status messages to stdout')
        parser.add_option('-d', '--make-dir', action='store_true', dest='make_dir', default=False,
                          help='create a directory for author and put the output file in it')
        parser.add_option('-o', '--output-file', dest='output_file', metavar='FILE',
                          help='specifies the output file')
        parser.add_option('-O', '--output-dir', dest='output_dir', metavar='DIR',
                          help='specifies the directory for output')
        if cls.uses_cover:
            if cls.cover_optional:
                parser.add_option('-c', '--with-cover', action='store_true', dest='with_cover', default=False,
                                  help='create default cover')
            parser.add_option('-C', '--image-cache', dest='image_cache', metavar='URL',
                              help='prefix for image download cache' +
                              (' (implies --with-cover)' if cls.cover_optional else ''))
        for option in cls.parser_options + cls.transform_options + cls.transform_flags:
            option.add(parser)

        options, input_filenames = parser.parse_args()

        if len(input_filenames) < 1:
            parser.print_help()
            return 1

        # Prepare additional args for parser.
        parser_args = {}
        for option in cls.parser_options:
            parser_args[option.name()] = option.value(options)
        # Prepare additional args for transform method.
        transform_args = {}
        for option in cls.transform_options:
            transform_args[option.name()] = option.value(options)
        # Add flags to transform_args, if any.
        transform_flags = [flag.name() for flag in cls.transform_flags if flag.value(options)]
        if transform_flags:
            transform_args['flags'] = transform_flags
        if options.verbose:
            transform_args['verbose'] = True
        # Add cover support, if any.
        if cls.uses_cover:
            if options.image_cache:
                def cover_class(*args, **kwargs):
                    return DefaultEbookCover(image_cache=options.image_cache, *args, **kwargs)
                transform_args['cover'] = cover_class
            elif not cls.cover_optional or options.with_cover:
                transform_args['cover'] = DefaultEbookCover

        # Do some real work
        try:
            for main_input in input_filenames:
                if options.verbose:
                    print main_input

            # Where to find input?
            if cls.uses_provider:
                path, fname = os.path.realpath(main_input).rsplit('/', 1)
                provider = DirDocProvider(path)
            else:
                provider = None

            # Where to write output?
            if not (options.output_file or options.output_dir):
                output_file = os.path.splitext(main_input)[0] + '.' + cls.ext
            else:
                output_file = options.output_file

            # Do the transformation.
            doc = WLDocument.from_file(main_input, provider=provider, **parser_args)
            transform = cls.transform
            if transform is None:
                transform = getattr(WLDocument, 'as_%s' % cls.ext)
            output = transform(doc, **transform_args)

            doc.save_output_file(output, output_file, options.output_dir, options.make_dir, cls.ext)

        except ParseError, e:
            print '%(file)s:%(name)s:%(message)s' % {
                'file': main_input,
                'name': e.__class__.__name__,
                'message': e
            }
