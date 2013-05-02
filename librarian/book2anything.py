#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from collections import namedtuple
import os.path
import optparse

from librarian import ParseError
from librarian.document import Document


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
    format_cls = None # A formats.Format subclass
    document_options = [] # List of Option objects for document options.
    format_options = [] # List of Option objects for format customization.
    build_options = [] # List of Option objects for build options.

    @classmethod
    def run(cls):
        # Parse commandline arguments
        usage = """Usage: %%prog [options] SOURCE [SOURCE...]
        Convert SOURCE files to %s.""" % cls.format_cls.format_name

        parser = optparse.OptionParser(usage=usage)

        parser.add_option('-v', '--verbose', 
                action='store_true', dest='verbose', default=False,
                help='print status messages to stdout')
        parser.add_option('-o', '--output-file',
                dest='output_file', metavar='FILE',
                help='specifies the output file')
        for option in cls.document_options + cls.format_options + cls.build_options:
            option.add(parser)

        options, input_filenames = parser.parse_args()

        if len(input_filenames) < 1:
            parser.print_help()
            return(1)

        # Prepare additional args for document.
        document_args = {}
        for option in cls.document_options:
            document_args[option.name()] = option.value(options)
        # Prepare additional args for format.
        format_args = {}
        for option in cls.format_options:
            format_args[option.name()] = option.value(options)
        # Prepare additional args for build.
        build_args = {}
        for option in cls.build_options:
            build_args[option.name()] = option.value(options)

        # Do some real work
        try:
            for main_input in input_filenames:
                if options.verbose:
                    print main_input

            # Do the transformation.
            doc = Document.from_file(main_input, **document_args)
            format_ = cls.format_cls(doc, **format_args)

            # Where to write output?
            if not options.output_file:
                output_file = os.path.splitext(main_input)[0] + '.' + format_.format_ext
            else:
                output_file = None
            
            output = format_.build(**build_args)
            output.save_as(output_file)

        except ParseError, e:
            print '%(file)s:%(name)s:%(message)s' % {
                'file': main_input,
                'name': e.__class__.__name__,
                'message': e
            }
