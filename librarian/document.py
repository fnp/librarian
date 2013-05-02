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
    # Do I use meta_context?
    def __init__(self, edoc, meta_context=None):
        self.edoc = edoc

        root_elem = edoc.getroot()
        if meta_context is not None:
            root_elem.meta_context = meta_context

        if not isinstance(root_elem, Section):
            if root_elem.tag != SSTNS('section'):
                raise ValidationError("Invalid root element. Found '%s', should be '%s'" % (
                    root_elem.tag, SSTNS('section')))
            else:
                raise ValidationError("Invalid class of root element. "
                    "Use librarian.parser.SSTParser.")

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

        parser = SSTParser()
        tree = etree.parse(StringIO(data.encode('utf-8')), parser)
        tree.xinclude()
        return cls(tree, *args, **kwargs)

    @property
    def meta(self):
        """ Document's metadata is root's metadata. """
        return self.edoc.getroot().meta
