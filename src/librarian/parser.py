# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from __future__ import unicode_literals

from collections import Counter

from librarian import ValidationError, NoDublinCore,  ParseError, NoProvider
from librarian import RDFNS
from librarian.cover import make_cover
from librarian import dcparser

from xml.parsers.expat import ExpatError
from lxml import etree
from lxml.etree import XMLSyntaxError, XSLTApplyError

import os
import re
import six


from .elements import WL_ELEMENTS


class WLElementLookup(etree.CustomElementClassLookup):
    def lookup(self, node_type, document, namespace, name):
        if node_type != 'element':
            return
        if namespace:
            return
        try:
            return WL_ELEMENTS[name]
        except KeyError:
            return


parser = etree.XMLParser()
parser.set_element_class_lookup(
    WLElementLookup()
)



class WLDocument(object):
    """Legacy class, to be replaced with documents.WLDocument."""
    LINE_SWAP_EXPR = re.compile(r'/\s', re.MULTILINE | re.UNICODE)
    provider = None

    def __init__(self, edoc, parse_dublincore=True, provider=None,
                 strict=False, meta_fallbacks=None):
        self.edoc = edoc
        self.provider = provider

        root_elem = edoc.getroot()

        dc_path = './/' + RDFNS('RDF')

        if root_elem.tag != 'utwor':
            raise ValidationError(
                "Invalid root element. Found '%s', should be 'utwor'"
                % root_elem.tag
            )

        if parse_dublincore:
            self.rdf_elem = root_elem.find(dc_path)

            if self.rdf_elem is None:
                raise NoDublinCore(
                    "Document must have a '%s' element." % RDFNS('RDF')
                )

            self.book_info = dcparser.BookInfo.from_element(
                self.rdf_elem, fallbacks=meta_fallbacks, strict=strict)
        else:
            self.book_info = None

    def get_statistics(self):
        def count_text(text, counter, in_fn=False):
            if text:
                text = re.sub(r'\s+', ' ', text)

                chars = len(text) if text.strip() else 0
                words = len(text.split()) if text.strip() else 0
                
                counter['chars'] += chars
                counter['words'] += words
                if not in_fn:
                    counter['chars_with_fn'] += chars
                    counter['words_with_fn'] += words
                
        def count(elem, counter, in_fn=False):
            if elem.tag in (RDFNS('RDF'), 'nota_red', 'abstrakt', 'uwaga', 'ekstra'):
                return
            if not in_fn and elem.tag in ('pa', 'pe', 'pr', 'pt', 'motyw'):
                in_fn = True
            count_text(elem.text, counter, in_fn=in_fn)
            for child in elem:
                count(child, counter, in_fn=in_fn)
                count_text(child.tail, counter, in_fn=in_fn)
            
            
        data = {
            "self": Counter(),
            "parts": [],
            "total": {
            }
        }

        count(self.edoc.getroot(), data['self'])
        for k, v in data['self'].items():
            data['total'][k] = v
        
        for part in self.parts(pass_part_errors=True):
            if isinstance(part, Exception):
                data['parts'].append((None, {}))
            else:
                data['parts'].append((part, part.get_statistics()))
                for k, v in data['parts'][-1][1]['total'].items():
                    data['total'][k] = data['total'].get(k, 0) + v
            
        return data

    @classmethod
    def from_bytes(cls, xml, *args, **kwargs):
        return cls.from_file(six.BytesIO(xml), *args, **kwargs)

    @classmethod
    def from_file(cls, xmlfile, *args, **kwargs):

        # first, prepare for parsing
        if isinstance(xmlfile, six.text_type):
            file = open(xmlfile, 'rb')
            try:
                data = file.read()
            finally:
                file.close()
        else:
            data = xmlfile.read()

        if not isinstance(data, six.text_type):
            data = data.decode('utf-8')

        data = data.replace(u'\ufeff', '')

        try:
            parser = etree.XMLParser(remove_blank_text=False)
            tree = etree.parse(six.BytesIO(data.encode('utf-8')), parser)

            return cls(tree, *args, **kwargs)
        except (ExpatError, XMLSyntaxError, XSLTApplyError) as e:
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

    def parts(self, pass_part_errors=False):
        if self.provider is None:
            raise NoProvider('No document provider supplied.')
        if self.book_info is None:
            raise NoDublinCore('No Dublin Core in document.')
        for part_uri in self.book_info.parts:
            try:
                yield self.from_file(
                    self.provider.by_uri(part_uri), provider=self.provider
                )
            except Exception as e:
                if pass_part_errors:
                    yield e
                else:
                    raise

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
                parts.append("*[%d][name() = '%s']" % (int(n)+1, tag))

        if parts[0] == '.':
            parts[0] = ''

        return '/'.join(parts)

    def transform(self, stylesheet, **options):
        return self.edoc.xslt(stylesheet, **options)

    def update_dc(self):
        if self.book_info:
            parent = self.rdf_elem.getparent()
            parent.replace(self.rdf_elem, self.book_info.to_etree(parent))

    def serialize(self):
        self.update_dc()
        return etree.tostring(self.edoc, encoding='unicode', pretty_print=True)

    def merge_chunks(self, chunk_dict):
        unmerged = []

        for key, data in chunk_dict.iteritems():
            try:
                xpath = self.path_to_xpath(key)
                node = self.edoc.xpath(xpath)[0]
                repl = etree.fromstring(
                    "<%s>%s</%s>" % (node.tag, data, node.tag)
                )
                node.getparent().replace(node, repl)
            except Exception as e:
                unmerged.append(repr((key, xpath, e)))

        return unmerged

    def clean_ed_note(self, note_tag='nota_red'):
        """ deletes forbidden tags from nota_red """

        for node in self.edoc.xpath('|'.join(
                '//%s//%s' % (note_tag, tag) for tag in
                ('pa', 'pe', 'pr', 'pt', 'begin', 'end', 'motyw'))):
            tail = node.tail
            node.clear()
            node.tag = 'span'
            node.tail = tail

    def fix_pa_akap(self):
        for pa in ('pa','pe','pr','pt'):
            for akap in self.edoc.findall(f'//{pa}/akap'):
                akap.getparent().set('blocks', 'true')
                if not akap.getparent().index(akap):
                    akap.set('inline', 'true')
            
    def editors(self):
        """Returns a set of all editors for book and its children.

        :returns: set of dcparser.Person objects
        """
        if self.book_info is None:
            raise NoDublinCore('No Dublin Core in document.')
        persons = set(self.book_info.editors
                      + self.book_info.technical_editors)
        for child in self.parts():
            persons.update(child.editors())
        if None in persons:
            persons.remove(None)
        return persons

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

    def as_fb2(self, *args, **kwargs):
        from librarian import fb2
        return fb2.transform(self, *args, **kwargs)

    def as_cover(self, cover_class=None, *args, **kwargs):
        if cover_class is None:
            cover_class = make_cover
        return cover_class(self.book_info, *args, **kwargs).output_file()

    # for debugging only
    def latex_dir(self, *args, **kwargs):
        kwargs['latex_dir'] = True
        from librarian import pdf
        return pdf.transform(self, *args, **kwargs)

    def save_output_file(self, output_file, output_path=None,
                         output_dir_path=None, make_author_dir=False,
                         ext=None):
        if output_dir_path:
            save_path = output_dir_path
            if make_author_dir:
                save_path = os.path.join(
                    save_path,
                    six.text_type(self.book_info.author).encode('utf-8')
                )
            save_path = os.path.join(save_path, self.book_info.url.slug)
            if ext:
                save_path += '.%s' % ext
        else:
            save_path = output_path

        output_file.save_as(save_path)
