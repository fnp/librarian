#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import optparse

from lxml import etree
from librarian import html
from slughifi import slughifi


BOOK_URL = 'http://wolnelektury.pl/katalog/lektura/'


if __name__ == '__main__':
    # Parse commandline arguments
    usage = """Usage: %prog [options] SOURCE [SOURCE...]
    Generate slugs for SOURCE."""

    parser = optparse.OptionParser(usage=usage)

    parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False,
        help='print status messages to stdout')
    parser.add_option('-f', '--force', action='store_true', dest='force', default=False,
        help='overwrite current identifiers')
    
    options, input_filenames = parser.parse_args()

    if len(input_filenames) < 1:
        parser.print_help()
        exit(1)

    # Do some real work
    for input_filename in input_filenames:
        if options.verbose:
            print input_filename
        
        doc = etree.parse(input_filename)
        try:
            title = doc.find('//{http://purl.org/dc/elements/1.1/}title').text
        except AttributeError:
            print '%s:error:Book title not found. Skipping.' % input_filename
            continue
        
        parent = ''
        try:
            parent_url = doc.find('//{http://purl.org/dc/elements/1.1/}relation.isPartOf').text
            parent = parent_url.rsplit('/', 1)[1] + ' '
        except AttributeError:
            pass
        except IndexError:
            print '%s:error:Invalid parent URL "%s". Skipping.' % (input_filename, parent_url)
            
        book_url = doc.find('//{http://purl.org/dc/elements/1.1/}identifier.url')
        if book_url is None:
            book_description = doc.find('//{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description')
            book_url = etree.SubElement(book_description, '{http://purl.org/dc/elements/1.1/}identifier.url')
        if not options.force and book_url.text.startswith('http://'):
            print '%s:Notice:Book already has identifier URL "%s". Skipping.' % (input_filename, book_url.text)
            continue
        
        book_url.text = BOOK_URL + slughifi(parent + title)[:60]

        doc.write(input_filename, xml_declaration=True, pretty_print=True, encoding='utf-8')

