# -*- coding: utf-8 -*-
# exception classes

class ParseError(Exception):
    
    def __init__(self, cause, message=None):
        self.cause = cause
        try:
            self.message = message or self.cause.message
        except:
            self.message = "No message."

class ValidationError(Exception):
    pass

class NoDublinCore(ValidationError):
    pass

class XMLNamespace(object):
    '''A handy structure to repsent names in an XML namespace.'''

    def __init__(self, uri):
        self.uri = uri

    def __call__(self, tag):
        return '{%s}%s' % (self.uri, tag)

    def __contains__(self, tag):
        return tag.startswith('{'+str(self)+'}')

    def __repr__(self):
        return 'XMLNamespace(%r)' % self.uri

    def __str__(self):
        return '%s' % self.uri

class EmptyNamespace(XMLNamespace):
    def __init__(self):
        super(EmptyNamespace, self).__init__('')

    def __call__(self, tag):
        return tag

# some common namespaces we use
RDFNS = XMLNamespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
DCNS = XMLNamespace('http://purl.org/dc/elements/1.1/')
XINS = XMLNamespace("http://www.w3.org/2001/XInclude")
XHTMLNS = XMLNamespace("http://www.w3.org/1999/xhtml")

WLNS = EmptyNamespace()

import lxml.etree as etree
import dcparser

DEFAULT_BOOKINFO = dcparser.BookInfo(
        { RDFNS('about'): u'http://wiki.wolnepodreczniki.pl/Lektury:Template'},\
        { DCNS('creator'): [u'Some, Author'],
          DCNS('title'): [u'Some Title'],
          DCNS('subject.period'): [u'Unknown'],
          DCNS('subject.type'): [u'Unknown'],
          DCNS('subject.genre'): [u'Unknown'],
          DCNS('date'): ['1970-01-01'],
          # DCNS('date'): [creation_date],
          DCNS('publisher'): [u"Fundacja Nowoczesna Polska"],
          DCNS('description'):
          [u"""Publikacja zrealizowana w ramach projektu
             Wolne Lektury (http://wolnelektury.pl). Reprodukcja cyfrowa
             wykonana przez Bibliotekę Narodową z egzemplarza
             pochodzącego ze zbiorów BN."""],
          DCNS('identifier.url'):
            [u"http://wolnelektury.pl/katalog/lektura/template"],
          DCNS('rights'):
            [u"Domena publiczna - zm. [OPIS STANU PRAWNEGO TEKSTU]"] })

def xinclude_forURI(uri):
    e = etree.Element( XINS("include") )
    e.set("href", uri)
    return etree.tostring(e, encoding=unicode)
    
def wrap_text(ocrtext, creation_date, bookinfo=DEFAULT_BOOKINFO):
    """Wrap the text within the minimal XML structure with a DC template."""
    bookinfo.created_at = creation_date
    
    dcstring = etree.tostring(bookinfo.to_etree(),\
        method='xml', encoding=unicode, pretty_print=True)

    return u'<utwor>\n' + dcstring + u'\n<plain-text>\n' + ocrtext +\
        u'\n</plain-text>\n</utwor>';