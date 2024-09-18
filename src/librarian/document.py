# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from collections import defaultdict, Counter
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
        self.counters = defaultdict(lambda: 1)
        tree.getroot().document = self

        self.preprocess()

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

    def preprocess(self):
        # Change slash-verses into real verses.
        for _e, elem in etree.iterwalk(self.tree, ('start',), 'strofa'):
            elem.preprocess()

    def assign_ids(self):
        # Assign IDs depth-first, to account for any <numeracja> inside.
        for _e, elem in etree.iterwalk(self.tree, events=('end',)):
            if getattr(elem, 'NUMBERING', None):
                elem.assign_id(self)

    @property
    def children(self):
        for part_uri in self.meta.parts or []:
            with self.provider.by_slug(part_uri.slug) as f:
                try:
                    yield type(self)(filename=f, provider=self.provider)
                except Exception as e:

                    yield e

    def build(self, builder, base_url=None, **kwargs):
        return builder(base_url=base_url).build(self, **kwargs)

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
