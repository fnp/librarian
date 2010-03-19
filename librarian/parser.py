# -*- coding: utf-8 -*-
from librarian import ValidationError, NoDublinCore, dcparser, ParseError
from xml.parsers.expat import ExpatError
from lxml import etree
from lxml.etree import XMLSyntaxError

import re
from StringIO import StringIO

class WLDocument(object):
    LINE_SWAP_EXPR = re.compile(r'/\s', re.MULTILINE | re.UNICODE);

    def __init__(self, edoc):
        self.edoc = edoc

        root_elem = edoc.getroot()
        rdf_ns = dcparser.BookInfo.RDF
        dc_path = './/' + rdf_ns('RDF')
        
        if root_elem.tag != 'utwor':
            raise ValidationError("Invalid root element. Found '%s', should be 'utwor'" % root_elem.tag)

        self.rdf_elem = root_elem.find(dc_path)

        if self.rdf_elem is None:
            raise NoDublinCore('Document has no DublinCore - which is required.')

        self.book_info = dcparser.BookInfo.from_element(self.rdf_elem)

    @classmethod
    def from_string(cls, xml, swap_endlines=False):
        return cls.from_file(StringIO(xml), swap_endlines)

    @classmethod
    def from_file(cls, xmlfile, swap_endlines=False):

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

        if swap_endlines:
            data = cls.LINE_SWAP_EXPR.sub(u'<br />\n', data)
    
        try:
            parser = etree.XMLParser(remove_blank_text=True)
            return cls( etree.parse(StringIO(data), parser) )
        except XMLSyntaxError, e:
             raise ParseError(e.message)            
        except ExpatError, e:
            raise ParseError(e.message)            

    def transform(self, stylesheet, **options):
        return self.edoc.xslt(stylesheet, **options)

    def update_dc(self):
        parent = self.rdf_elem.getparent()
        parent.replace( self.rdf_elem, self.book_info.to_etree(parent) )

    def serialize(self):
        self.update_dc()
        return etree.tostring(self.edoc, encoding=unicode, pretty_print=True)
