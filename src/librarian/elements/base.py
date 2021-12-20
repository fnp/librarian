# -*- coding: utf-8

import re
from lxml import etree
from librarian import dcparser, RDFNS
from librarian.util import get_translation


class WLElement(etree.ElementBase):
    SECTION_PRECEDENCE = None

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

    text_substitutions = [
        (u'---', u'—'),
        (u'--', u'–'),
        #(u'...', u'…'),  # Temporary turnoff for epub
        (u',,', u'„'),
        (u'"', u'”'),
        ('\ufeff', ''),

        ("'", "\u2019"),    # This was enabled for epub.
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
            # FIXME: TEmporary turnoff
#        text = re.sub(r'\s+', ' ', text)
### TODO: Added now for epub

        if getattr(builder, 'hyphenator', None) is not None:
            newt = ''
            wlist = re.compile(r'\w+|[^\w]', re.UNICODE).findall(text)
            for w in wlist:
                newt += builder.hyphenator.inserted(w, u'\u00AD')
            text = newt

        text = re.sub(r'(?<=\s\w)\s+', u'\u00A0', text)

        return text

    def _build_inner(self, builder, build_method):
        child_count = len(self)
        if self.CAN_HAVE_TEXT and self.text:
            text = self.normalize_text(self.text, builder)
            if self.STRIP:
                text = text.lstrip()
                if not child_count:
                    text = text.rstrip()
            builder.push_text(text)
        for i, child in enumerate(self):
            if isinstance(child, WLElement):
                getattr(child, build_method)(builder)
            if self.CAN_HAVE_TEXT and child.tail:
                text = self.normalize_text(child.tail, builder)
                if self.STRIP and i == child_count - 1:
                    text = text.rstrip()
                builder.push_text(text)

    def _txt_build_inner(self, builder):
        self._build_inner(builder, 'txt_build')

    def txt_build(self, builder):
        if hasattr(self, 'TXT_LEGACY_TOP_MARGIN'):
            builder.push_legacy_margin(self.TXT_LEGACY_TOP_MARGIN)
        else:
            builder.push_margin(self.TXT_TOP_MARGIN)
        builder.push_text(self.TXT_PREFIX, True)
        self._txt_build_inner(builder)
        builder.push_text(self.TXT_SUFFIX, True)
        if hasattr(self, 'TXT_LEGACY_BOTTOM_MARGIN'):
            builder.push_legacy_margin(self.TXT_LEGACY_BOTTOM_MARGIN)
        else:
            builder.push_margin(self.TXT_BOTTOM_MARGIN)

    def _html_build_inner(self, builder):
        self._build_inner(builder, 'html_build')

    def get_html_attr(self, builder):
        attr = self.HTML_ATTR.copy()
        if self.HTML_CLASS:
            attr['class'] = self.HTML_CLASS
        # always copy the id attribute (?)
        if self.attrib.get('id'):
            attr['id'] = self.attrib['id']
        elif '_compat_section_id' in self.attrib:
            attr['id'] = self.attrib['_compat_section_id']
        return attr

    def html_build(self, builder):
        if self.HTML_TAG:
            builder.start_element(
                self.HTML_TAG,
                self.get_html_attr(builder),
            )

        self._html_build_inner(builder)
        if self.HTML_TAG:
            builder.end_element()

    def _epub_build_inner(self, builder):
        self._build_inner(builder, 'epub_build')

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
            builder.start_element(
                self.EPUB_TAG,
                attr
            )

        self._epub_build_inner(builder)
        if self.EPUB_TAG:
            builder.end_element()

    def validate(self):
        from librarian.elements.masters import Master
        from librarian.elements.blocks import DlugiCytat, PoezjaCyt
        from librarian.elements.footnotes import Footnote

        if self.SECTION_PRECEDENCE:
            assert isinstance(self.getparent(), (Master, DlugiCytat, PoezjaCyt, Footnote)), \
                    'Header {} inside a <{}> instead of a master.'.format(
                            etree.tostring(self), self.getparent().tag)

        for c in self:
            if isinstance(c, WLElement):
                c.validate()


    def sanitize(self):
        # TODO: Remove insanity here.
        for e in self:
            if isinstance(e, WLElement):
                e.sanitize()
