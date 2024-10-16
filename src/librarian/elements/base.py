# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import copy
import re
from lxml import etree
from librarian import dcparser, RDFNS
from librarian.util import get_translation

def last_words(text, n):
    words = []
    for w in reversed(text.split()):
        words.append(w)
        if len(w) > 2:
            n -= 1
            if not n: break
    if n:
        return n, text
    else:
        return n, ' '.join(reversed(words))


class WLElement(etree.ElementBase):
    SECTION_PRECEDENCE = None
    ASIDE = False

    TXT_TOP_MARGIN = 0
    TXT_BOTTOM_MARGIN = 0
    TXT_PREFIX = ""
    TXT_SUFFIX = ""

    HTML_TAG = None
    HTML_ATTR = {}
    HTML_CLASS = None

    EPUB_TAG = None
    EPUB_ATTR = {}
    EPUB_CLASS = None
    EPUB_START_CHUNK = False
   
    CAN_HAVE_TEXT = True
    STRIP = False
    NUMBERING = None

    text_substitutions = [
        ('---', '—'),
        ('--', '–'),
        ('...', '…'),
        (',,', '„'),
        ('"', '”'),
        ('\ufeff', ''),
        ("'", "\u2019"),
    ]

    @property
    def meta_object(self):
        if not hasattr(self, '_meta_object'):
            elem = self.find(RDFNS('RDF'))
            if elem is not None:
                self._meta_object = dcparser.BookInfo.from_element(elem)
            else:
                self._meta_object = None
        return self._meta_object

    @property
    def meta(self):
        if self.meta_object is not None:
            return self.meta_object
        else:
            if self.getparent() is not None:
                return self.getparent().meta
            else:
                return self.document.base_meta

    @property
    def gettext(self):
        return get_translation(self.meta.language).gettext

    def in_context_of(self, setting):
        parent = self.getparent()
        if parent is None:
            return False
        try:
            return getattr(parent, setting)
        except AttributeError:
            return parent.in_context_of(setting)

    def get_context_map(self, setting, key, default=None):
        parent = self.getparent()
        if parent is None:
            return default
        try:
            return getattr(parent, setting)[key]
        except AttributeError:
            return parent.get_context_map(setting, key, default)

    def signal(self, signal):
        parent = self.getparent()
        if parent is not None:
            parent.signal(signal)
    
    def raw_printable_text(self, builder):
        from librarian.html import raw_printable_text

        # TODO: podtagi, wyroznienia, etc
        t = ''
        t += self.normalize_text(self.text, builder)
        for c in self:
            if not isinstance(c, WLElement):
                continue
            if c.tag not in ('pe', 'pa', 'pt', 'pr', 'motyw'):
                t += c.raw_printable_text(builder)
            t += self.normalize_text(c.tail, builder)
        return t
    
    def normalize_text(self, text, builder):
        text = text or ''
        for e, s in self.text_substitutions:
            text = text.replace(e, s)

        if getattr(builder, 'normalize_whitespace', False):
            text = re.sub(r'\s+', ' ', text)

        if getattr(builder, 'hyphenator', None) is not None:
            newt = ''
            wlist = re.compile(r'\w+|[^\w]', re.UNICODE).findall(text)
            for w in wlist:
                newt += builder.hyphenator.inserted(w, '\u00AD')
            text = newt

        if builder.orphans:
            text = re.sub(r'(?<=\s\w)\s+', '\u00A0', text)

        return text

    def build_inner(self, builder):
        build_method = builder.build_method_fn
        child_count = len(self)
        if self.CAN_HAVE_TEXT and self.text:
            text = self.normalize_text(self.text, builder)
            if self.STRIP:
                text = text.lstrip()
                if not child_count:
                    text = text.rstrip()
            builder.push_text(text)
        for i, child in enumerate(self):
            real_child_count = 0
            if isinstance(child, WLElement):
                getattr(child, build_method)(builder)
                self.after_child(builder, real_child_count)
                real_child_count += 1

            # FIXME base builder api
            elif getattr(builder, 'debug', False) and child.tag is etree.Comment:
                builder.process_comment(child)
            if self.CAN_HAVE_TEXT and child.tail:
                text = self.normalize_text(child.tail, builder)
                if self.STRIP and i == child_count - 1:
                    text = text.rstrip()
                builder.push_text(text)

    def after_child(self, builder, child_count):
        fn = getattr(builder, 'after_child_fn', None)
        if fn:
            getattr(self, builder.after_child_fn)(builder, child_count)

    def txt_after_child(self, builder, child_count):
        pass

    def txt_build_inner(self, builder):
        self.build_inner(builder)

    def txt_build(self, builder):
        builder.push_margin(self.TXT_TOP_MARGIN)
        builder.push_text(self.TXT_PREFIX, True)
        self.txt_build_inner(builder)
        builder.push_text(self.TXT_SUFFIX, True)
        builder.push_margin(self.TXT_BOTTOM_MARGIN)

    def html_build_inner(self, builder):
        self.build_inner(builder)

    def get_html_attr(self, builder):
        attr = self.HTML_ATTR.copy()
        if self.HTML_CLASS:
            attr['class'] = self.HTML_CLASS
        if builder.with_ids:
            # always copy the id attribute (?)
            if self.attrib.get('id'):
                attr['id'] = self.attrib['id']
            if self.attrib.get('_id'):
                attr['id'] = self.attrib['_id']
        return attr

    def html_build(self, builder):
        # Do we need a number?
        numbering = self.numbering
        if numbering == 'main':
            if builder.with_numbering and self.has_visible_numbering:
                builder.add_visible_number(self)

        if self.HTML_TAG:
            builder.start_element(
                self.HTML_TAG,
                self.get_html_attr(builder),
            )

        self.html_build_inner(builder)
        if self.HTML_TAG:
            builder.end_element()

    def epub_build_inner(self, builder):
        self.build_inner(builder)

    def get_epub_attr(self, builder):
        attr = self.EPUB_ATTR.copy()
        if self.EPUB_CLASS:
            attr['class'] = self.EPUB_CLASS
        return attr

    def epub_build(self, builder):
        from librarian.elements.masters import Master

        # TEMPORARY
        self.CAN_HAVE_TEXT = True
        self.STRIP = False

        start_chunk = self.EPUB_START_CHUNK and isinstance(self.getparent(), Master)

        if start_chunk:
            builder.start_chunk()

        fragment = None
        if self.SECTION_PRECEDENCE and not self.in_context_of('NO_TOC'):
            if not start_chunk:
                fragment = 'sub%d' % builder.assign_section_number()
                self.attrib['id'] = fragment

            builder.add_toc_entry(
                fragment,
                self.raw_printable_text(builder),
                self.SECTION_PRECEDENCE
            )
            
        if self.EPUB_TAG:
            attr = self.get_epub_attr(builder)
            if fragment:
                attr['id'] = fragment
            if builder.debug:
                chunkno, sourceline = 0, self.sourceline
                if builder.splits:
                    chunkno, sourceline = len(builder.splits), sourceline - builder.splits[-1]
                attr['data-debug'] = f'{chunkno}:{sourceline}'
            builder.start_element(
                self.EPUB_TAG,
                attr
            )

        self.epub_build_inner(builder)
        if self.EPUB_TAG:
            builder.end_element()

    def validate(self):
        from librarian.elements.masters import Master
        from librarian.elements.blocks import DlugiCytat, PoezjaCyt
        from librarian.elements.footnotes import Footnote

        if self.SECTION_PRECEDENCE:
            assert isinstance(self.getparent(), (Master, DlugiCytat, PoezjaCyt, Footnote)), \
                    'Header {} inside a <{}> instead of a master.'.format(
                            etree.tostring(self, encoding='unicode'), self.getparent().tag)

        for c in self:
            if isinstance(c, WLElement):
                c.validate()


    def sanitize(self):
        # TODO: Remove insanity here.
        for e in self:
            if isinstance(e, WLElement):
                e.sanitize()

    def snip(self, words, before=None, sub=False):
        if sub and self.ASIDE:
            return words, []

        snippet = []
        if before is not None:
            i = self.index(before)
        else:
            i = len(self)

        while i > 0:
            i -= 1
            if self[i].tail:
                if words:
                    words, text = last_words(self[i].tail, words)
                    snippet = [('text', text)] + snippet

            if words:
                words, subsnip = self[i].snip(words, sub=True)
                snippet = subsnip + snippet

        if words and self.text:
            words, text = last_words(self.text, words)
            snippet = [('text', text)] + snippet
                    
        snippet = [('start', self.tag, self.attrib)] + snippet + [('end',)]

        if not sub and words and not self.ASIDE:
            # do we dare go up?
            parent = self.getparent()
            if parent is not None and parent.CAN_HAVE_TEXT:
                words, parsnip = parent.snip(words, before=self)
                return words, parsnip[:-1] + snippet + parsnip[-1:]

        return words, snippet

    def get_snippet(self, words=15):
        from librarian.parser import parser

        words, snippet = self.getparent().snip(words=words, before=self)
        
        cursor = snipelem = parser.makeelement('snippet')
        snipelem._meta_object = self.meta
        for s in snippet:
            if s[0] == 'start':
                elem = parser.makeelement(s[1], **s[2])
                cursor.append(elem)
                cursor = elem
            elif s[0] == 'end':
                cursor = cursor.getparent()
            else:
                if len(cursor):
                    cursor[-1].tail = (cursor[-1].tail or '') + s[1]
                else:
                    cursor.text = (cursor.text or '') + s[1]

        return snipelem

    @property
    def numbering(self):
        numbering = self.NUMBERING
        if numbering is None or self.in_context_of('DISABLE_NUMBERING'):
            return None
        numbering = self.get_context_map('SUPPRESS_NUMBERING', numbering, numbering)
        return numbering

    @property
    def id_prefix(self):
        prefix = self.numbering
        if prefix == 'main':
            # TODO: self.context.main_numbering_prefix
            prefix = 'f' # default numbering prefix
        return prefix

    def assign_id(self, document):
        numbering = self.numbering
        if numbering:
            number = str(document.counters[numbering])
            self.attrib['_id'] = self.id_prefix + number
            document.counters[numbering] += 1

            if numbering == 'main':
                self.attrib['_visible_numbering'] = str(document.counters['_visible'])
                document.counters['_visible'] += 1

            if numbering == 'fn':
                self.attrib['_visible_numbering'] = number

    def get_link(self):
        return self.attrib.get('_id') or self.getparent().get_link()


class Snippet(WLElement):
    pass
