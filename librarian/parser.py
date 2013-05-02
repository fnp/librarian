# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from lxml import etree
from . import DCNS, SSTNS
from . import core, meta


class SSTParser(etree.XMLParser):
    """ XML parser using relevant element classes. """
    def __init__(self):
        super(SSTParser, self).__init__(remove_blank_text=False)
        lookup = etree.ElementNamespaceClassLookup()
        self.set_element_class_lookup(lookup)

        # Define core language tags.
        sst_ns = lookup.get_namespace(SSTNS.uri)
        sst_ns['aside'] = core.Aside
        sst_ns['div'] = core.Div
        sst_ns['header'] = core.Header
        sst_ns['section'] = core.Section
        sst_ns['span'] = core.Span
        sst_ns['metadata'] = meta.Metadata

        # Define any special metadata.
        dc_ns = lookup.get_namespace(DCNS.uri)
        dc_ns['creator'] = meta.Person
        dc_ns['identifier'] = meta.Identifier
