# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from librarian import ValidationError, NoDublinCore,  ParseError, NoProvider
from librarian import RDFNS
from librarian import dcparser

from xml.parsers.expat import ExpatError
from lxml import etree
from lxml.etree import XMLSyntaxError, XSLTApplyError

import os
import re
from StringIO import StringIO

class WLDocument(object):
    LINE_SWAP_EXPR = re.compile(r'/\s', re.MULTILINE | re.UNICODE)
    provider = None

    def __init__(self, edoc, parse_dublincore=True, provider=None):
        self.edoc = edoc
        self.provider = provider

        root_elem = edoc.getroot()

        dc_path = './/' + RDFNS('RDF')

        if root_elem.tag != 'utwor':
            raise ValidationError("Invalid root element. Found '%s', should be 'utwor'" % root_elem.tag)

        if parse_dublincore:
            self.rdf_elem = root_elem.find(dc_path)

            if self.rdf_elem is None:
                raise NoDublinCore('Document has no DublinCore - which is required.')

            self.book_info = dcparser.BookInfo.from_element(self.rdf_elem)
        else:
            self.book_info = None

    @classmethod
    def from_string(cls, xml, *args, **kwargs):
        return cls.from_file(StringIO(xml), *args, **kwargs)

    @classmethod
    def from_file(cls, xmlfile, parse_dublincore=True, provider=None):

        # first, prepare for parsing
        if isinstance(xmlfile, basestring):
            file = open(xmlfile, 'rb')
            try:
                data = file.read()
            finally:
                file.close()
        else:
            data = xmlfile.read()

        if not isinstance(data, unicode):
            data = data.decode('utf-8')

        data = data.replace(u'\ufeff', '')

        try:
            parser = etree.XMLParser(remove_blank_text=False)
            tree = etree.parse(StringIO(data.encode('utf-8')), parser)

            return cls(tree, parse_dublincore=parse_dublincore, provider=provider)
        except (ExpatError, XMLSyntaxError, XSLTApplyError), e:
            raise ParseError(e)

    def swap_endlines(self):
        """Converts line breaks in stanzas into <br/> tags."""
        # only swap inside stanzas
        for elem in self.edoc.iter('strofa'):
            for child in list(elem):
                if child.tail:
                    chunks = self.LINE_SWAP_EXPR.split(child.tail)
                    ins_index = elem.index(child) + 1
                    while len(chunks) > 1:
                        ins = etree.Element('br')
                        ins.tail = chunks.pop()
                        elem.insert(ins_index, ins)
                    child.tail = chunks.pop(0)
            if elem.text:
                chunks = self.LINE_SWAP_EXPR.split(elem.text)
                while len(chunks) > 1:
                    ins = etree.Element('br')
                    ins.tail = chunks.pop()
                    elem.insert(0, ins)
                elem.text = chunks.pop(0)

    def parts(self):
        if self.provider is None:
            raise NoProvider('No document provider supplied.')
        if self.book_info is None:
            raise NoDublinCore('No Dublin Core in document.')
        for part_uri in self.book_info.parts:
            yield self.from_file(self.provider.by_uri(part_uri),
                    provider=self.provider)

    def chunk(self, path):
        # convert the path to XPath
        expr = self.path_to_xpath(path)
        elems = self.edoc.xpath(expr)

        if len(elems) == 0:
            return None
        else:
            return elems[0]

    def path_to_xpath(self, path):
        parts = []

        for part in path.split('/'):
            match = re.match(r'([^\[]+)\[(\d+)\]', part)
            if not match:
                parts.append(part)
            else:
                tag, n = match.groups()
                parts.append("*[%d][name() = '%s']" % (int(n)+1, tag) )

        if parts[0] == '.':
            parts[0] = ''

        return '/'.join(parts)

    def transform(self, stylesheet, **options):
        return self.edoc.xslt(stylesheet, **options)

    def update_dc(self):
        if self.book_info:
            parent = self.rdf_elem.getparent()
            parent.replace( self.rdf_elem, self.book_info.to_etree(parent) )

    def serialize(self):
        self.update_dc()
        return etree.tostring(self.edoc, encoding=unicode, pretty_print=True)

    def merge_chunks(self, chunk_dict):
        unmerged = []

        for key, data in chunk_dict.iteritems():
            try:
                xpath = self.path_to_xpath(key)
                node = self.edoc.xpath(xpath)[0]
                repl = etree.fromstring(u"<%s>%s</%s>" %(node.tag, data, node.tag) )
                node.getparent().replace(node, repl);
            except Exception, e:
                unmerged.append( repr( (key, xpath, e) ) )

        return unmerged

    def clean_ed_note(self):
        """ deletes forbidden tags from nota_red """

        for node in self.edoc.xpath('|'.join('//nota_red//%s' % tag for tag in
                    ('pa', 'pe', 'pr', 'pt', 'begin', 'end', 'motyw'))):
            tail = node.tail
            node.clear()
            node.tag = 'span'
            node.tail = tail

    # Converters

    def as_html(self, *args, **kwargs):
        from librarian import html
        return html.transform(self, *args, **kwargs)

    def as_text(self, *args, **kwargs):
        from librarian import text
        return text.transform(self, *args, **kwargs)

    def as_epub(self, *args, **kwargs):
        from librarian import epub
        return epub.transform(self, *args, **kwargs)

    def as_pdf(self, *args, **kwargs):
        from librarian import pdf
        return pdf.transform(self, *args, **kwargs)

    def as_mobi(self, *args, **kwargs):
        from librarian import mobi
        return mobi.transform(self, *args, **kwargs)

    def save_output_file(self, output_file, output_path=None,
            output_dir_path=None, make_author_dir=False, ext=None):
        if output_dir_path:
            save_path = output_dir_path
            if make_author_dir:
                save_path = os.path.join(save_path,
                        unicode(self.book_info.author).encode('utf-8'))
            save_path = os.path.join(save_path, self.book_info.slug)
            if ext:
                save_path += '.%s' % ext
        else:
            save_path = output_path

        output_file.save_as(save_path)
