# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from StringIO import StringIO
from lxml import etree
from . import SSTNS
from .core import Section
from .parser import SSTParser


class Document(object):
    def __init__(self, edoc, meta_context=None):
        self.edoc = edoc
        root_elem = edoc.getroot()
        # Do I use meta_context?
        if meta_context is not None:
            root_elem.meta_context = meta_context
        self.validate()

    def validate(self):
        root_elem = self.edoc.getroot()
        if not isinstance(root_elem, Section):
            if root_elem.tag != SSTNS('section'):
                if root_elem.tag == 'section':
                    for element in root_elem.iter():
                        if element.tag in ('section', 'header', 'div', 'span', 'aside', 'metadata'):
                            element.tag = str(SSTNS(element.tag))

                    parser = SSTParser()
                    tree = etree.parse(StringIO(etree.tostring(root_elem)), parser)
                    tree.xinclude()
                    self.edoc = tree
                else:
                    raise ValueError("Invalid root element. Found '%s', should be '%s'" % (
                        root_elem.tag, SSTNS('section')))
            else:
                raise ValueError("Invalid class of root element. Use librarian.parser.SSTParser.")

    @classmethod
    def from_string(cls, xml, *args, **kwargs):
        return cls.from_file(StringIO(xml), *args, **kwargs)

    @classmethod
    def from_file(cls, xmlfile, *args, **kwargs):
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
        # This is bad. The editor shouldn't spew unknown HTML entities.
        data = data.replace(u'&nbsp;', u'\u00a0')

        parser = SSTParser()
        tree = etree.parse(StringIO(data.encode('utf-8')), parser)
        tree.xinclude()
        return cls(tree, *args, **kwargs)

    @property
    def meta(self):
        """ Document's metadata is root's metadata. """
        return self.edoc.getroot().meta
