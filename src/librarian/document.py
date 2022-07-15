import gettext
import os
import re
from lxml import etree
import six
from .parser import parser
from . import dcparser, DCNS, DirDocProvider
from .functions import lang_code_3to2


class WLDocument:
    def __init__(self, filename=None, url=None, provider=None):
        source = filename or six.moves.urllib.request.urlopen(url)
        tree = etree.parse(source, parser=parser)
        self.tree = tree
        tree.getroot().document = self
        self.base_meta = dcparser.BookInfo({}, {
            DCNS('language'): ["pol"],
        }, validate_required=False)

        self.provider = provider if provider is not None else DirDocProvider('.')

        self.tree.getroot().validate()

    @property
    def meta(self):
        # Allow metadata of the master element as document meta.
        #master = self.tree.getroot()[-1]
        return self.tree.getroot().meta
        return master.meta

    @property
    def children(self):
        for part_uri in self.meta.parts or []:
            yield type(self)(
                filename=self.provider.by_slug(part_uri.slug),
                provider=self.provider
            )
            
    
    def build(self, builder, base_url=None, **kwargs):
        return builder(base_url=base_url).build(self, **kwargs)

    def _compat_assign_ordered_ids(self):
        """
        Compatibility: ids in document order, to be roughly compatible with legacy
        footnote ids. Just for testing consistency, change to some sane identifiers
        at convenience.
        """
        EXPR = re.compile(r'/\s', re.MULTILINE | re.UNICODE)
        def _compat_assign_ordered_ids_in_elem(elem, i):
            elem.attrib['_compat_ordered_id'] = str(i)
            i += 1
            if getattr(elem, 'HTML_CLASS', None) == 'stanza':
                if elem.text:
                    i += len(EXPR.split(elem.text)) - 1
                for sub in elem:
                    i = _compat_assign_ordered_ids_in_elem(sub, i)
                    if sub.tail:
                        i += len(EXPR.split(sub.tail)) - 1
            else:
                if elem.tag in ('uwaga', 'extra'):
                    return i
                for sub in elem:
                    i = _compat_assign_ordered_ids_in_elem(sub, i)
            return i

        _compat_assign_ordered_ids_in_elem(self.tree.getroot(), 4)

    def _compat_assign_section_ids(self):
        """
        Ids in master-section order. These need to be compatible with the
        #secN anchors used by WL search results page to link to fragments.
        """
        def _compat_assigns_section_ids_in_elem(elem, prefix='sec'):
            for i, child in enumerate(elem):
                idfier = '{}{}'.format(prefix, i + 1)
                child.attrib['_compat_section_id'] = idfier
                _compat_assigns_section_ids_in_elem(child, idfier + '-')
        _compat_assigns_section_ids_in_elem(self.tree.getroot().master)


    def editors(self):
        persons = set(self.meta.editors
                      + self.meta.technical_editors)
        for child in self.children:
            persons.update(child.editors())
        if None in persons:
            persons.remove(None)
        return persons

