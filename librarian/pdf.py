# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import os
import os.path
import shutil
from StringIO import StringIO
from tempfile import mkdtemp
import re

from Texml.processor import process
from lxml import etree
from lxml.etree import XMLSyntaxError, XSLTApplyError

from librarian.parser import WLDocument
from librarian import ParseError
from librarian import functions

functions.reg_substitute_entities()

STYLESHEETS = {
    'wl2tex': 'xslt/wl2tex.xslt',
}


def insert_tags(doc, split_re, tagname):
    print tagname
    for elem in doc.iter():
        if elem.text:
            chunks = split_re.split(elem.text)
            elem.text = chunks.pop(0)
            while chunks:
                ins = etree.Element(tagname)
                ins.tail = chunks.pop()
                elem.insert(0, ins)
        if elem.tail:
            chunks = split_re.split(elem.tail)
            parent = elem.getparent()
            ins_index = parent.index(elem) + 1
            elem.tail = chunks.pop(0)
            while chunks:
                ins = etree.Element(tagname)
                ins.tail = chunks.pop(0)
                parent.insert(ins_index, ins)


def substitute_hyphens(doc):
    insert_tags(doc, 
                re.compile("(?<=[^-\s])-(?=[^-\s])"),
                "dywiz")


def fix_hanging(doc):
    insert_tags(doc, 
                re.compile("(?<=\s\w)\s+"),
                "nbsp")


def get_stylesheet(name):
    return os.path.join(os.path.dirname(__file__), STYLESHEETS[name])

def transform(provider, slug, output_file=None, output_dir=None):
    """ produces a pdf file

    provider is a DocProvider
    either output_file (a file-like object) or output_dir (path to file/dir) should be specified
    if output_dir is specified, file will be written to <output_dir>/<author>/<slug>.pdf
    """

    # Parse XSLT
    try:
        style_filename = get_stylesheet("wl2tex")
        style = etree.parse(style_filename)

        document = load_including_children(provider, slug)

        substitute_hyphens(document.edoc)
        fix_hanging(document.edoc)
        
        print etree.tostring(document.edoc)

        # if output to dir, create the file
        if output_dir is not None:
            author = unicode(document.book_info.author)
            output_dir = os.path.join(output_dir, author)

        texml = document.transform(style)
        del document # no longer needed large object :)

        temp = mkdtemp('wl2pdf-')
        tex_path = os.path.join(temp, 'doc.tex')
        fout = open(tex_path, 'w')
        process(StringIO(texml), fout, 'utf8', 255, 0, 0)
        fout.close()
        del texml

        print "pdflatex -output-directory %s %s" % (temp, os.path.join(temp, 'doc.tex'))
        if os.system("pdflatex -output-directory %s %s" % (temp, os.path.join(temp, 'doc.tex'))):
            raise ParseError("Error parsing .tex file")

        pdf_path = os.path.join(temp, 'doc.pdf')
        if output_dir is not None:
            try:
                os.makedirs(output_dir)
            except OSError:
                pass
            output_path = os.path.join(output_dir, '%s.pdf' % slug)
            shutil.move(pdf_path, output_path)
        else:
            with open(pdf_path) as f:
                output_file.write(f.read())
            output_file.close()

        return True
    except (XMLSyntaxError, XSLTApplyError), e:
        raise ParseError(e)


def load_including_children(provider, slug=None, uri=None):
    """ makes one big xml file with children inserted at end 
    either slug or uri must be provided
    """

    if uri:
        f = provider.by_uri(uri)
    elif slug:
        f = provider[slug]
    else:
        raise ValueError('Neither slug nor URI provided for a book.')

    document = WLDocument.from_file(f, True,
        parse_dublincore=True,
        preserve_lines=False)

    for child_uri in document.book_info.parts:
        child = load_including_children(provider, uri=child_uri)
        document.edoc.getroot().append(child.edoc.getroot())

    return document


if __name__ == '__main__':
    import sys
    from librarian import DirDocProvider

    if len(sys.argv) < 2:
        print >> sys.stderr, 'Usage: python pdf.py <input file>'
        sys.exit(1)

    main_input = sys.argv[1]
    basepath, ext = os.path.splitext(main_input)
    path, slug = os.path.realpath(basepath).rsplit('/', 1)
    provider = DirDocProvider(path)
    transform(provider, slug, output_dir=path)

