# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from collections import Counter
import gettext
import os
import re
import urllib.request
from lxml import etree
from .parser import parser
from . import dcparser, DCNS, RDFNS, DirDocProvider
from .functions import lang_code_3to2


class WLDocument:
    def __init__(self, filename=None, url=None, provider=None):
        source = filename or urllib.request.urlopen(url)
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
            with self.provider.by_slug(part_uri.slug) as f:
                try:
                    yield type(self)(filename=f, provider=self.provider, child=True)
                except Exception as e:

                    yield e

    def build(self, builder, base_url=None, **kwargs):
        return builder(base_url=base_url).build(self, **kwargs)

    def assign_ids(self, existing=None):
        # Find all existing IDs.
        existing = existing or set()
        que = [self.tree.getroot()]
        while que:
            item = que.pop(0)
            try:
                item.normalize_insides()
            except AttributeError:
                pass
            existing.add(item.attrib.get('id'))
            que.extend(item)

        i = 1
        que = [self.tree.getroot()]
        while que:
            item = que.pop(0)
            que.extend(item)
            if item.attrib.get('id'):
                continue
            if not getattr(item, 'SHOULD_HAVE_ID', False):
                continue
            while f'e{i}' in existing:
                i += 1
            item.attrib['id'] = f'e{i}'
            i += 1

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
                try:
                    child.attrib['_compat_section_id'] = idfier
                except:
                    pass
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

    def references(self):
        return self.tree.findall('.//ref')

    def get_statistics(self):
        def count_text(text, counter, in_fn=False, stanza=False):
            if text:
                text = re.sub(r'\s+', ' ', text)

                chars = len(text) if text.strip() else 0
                words = len(text.split()) if text.strip() else 0

                counter['chars_with_fn'] += chars
                counter['words_with_fn'] += words
                if not in_fn:
                    counter['chars'] += chars
                    counter['words'] += words
                if not stanza:
                    counter['chars_out_verse_with_fn'] += chars
                    if not in_fn:
                        counter['chars_out_verse'] += chars

        def count(elem, counter, in_fn=False, stanza=False):
            if elem.tag in (RDFNS('RDF'), 'nota_red', 'abstrakt', 'uwaga', 'ekstra'):
                return
            if not in_fn and elem.tag in ('pa', 'pe', 'pr', 'pt', 'motyw'):
                in_fn = True
            if elem.tag == 'strofa':
                # count verses now
                #verses = len(elem.findall('.//br')) + 1
                verses = list(elem.get_verses())
                counter['verses_with_fn'] += len(verses)
                if not in_fn:
                    counter['verses'] += len(verses)
                stanza = True

                for child in verses:
                    count(child, counter, in_fn=in_fn, stanza=True)
            else:
                count_text(elem.text, counter, in_fn=in_fn, stanza=stanza)
                for child in elem:
                    count(child, counter, in_fn=in_fn, stanza=stanza)
                    count_text(child.tail, counter, in_fn=in_fn, stanza=stanza)

        data = {
            "self": Counter(),
            "parts": [],
            "total": {
            }
        }

        count(self.tree.getroot(), data['self'])
        for k, v in data['self'].items():
            data['total'][k] = v

        for part in self.children:
            if isinstance(part, Exception):
                data['parts'].append((None, {'error': part}))
            else:
                data['parts'].append((part, part.get_statistics()))
                for k, v in data['parts'][-1][1]['total'].items():
                    data['total'][k] = data['total'].get(k, 0) + v

        return data
