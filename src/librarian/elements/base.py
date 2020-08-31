# -*- coding: utf-8

import re
from lxml import etree
from librarian import dcparser, RDFNS


class WLElement(etree.ElementBase):
    TXT_TOP_MARGIN = 0
    TXT_BOTTOM_MARGIN = 0
    TXT_PREFIX = ""
    TXT_SUFFIX = ""

    HTML_TAG = None
    HTML_ATTR = {}
    HTML_CLASS = None
    HTML_SECTION = False
    
    CAN_HAVE_TEXT = True
    STRIP = False

    text_substitutions = [
        (u'---', u'—'),
        (u'--', u'–'),
        (u'...', u'…'),
        (u',,', u'„'),
        (u'"', u'”'),
        ('\ufeff', ''),
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
    
    def normalize_text(self, text):
        text = text or ''
        for e, s in self.text_substitutions:
            text = text.replace(e, s)
        text = re.sub(r'\s+', ' ', text)
        return text

    def _build_inner(self, builder, build_method):
        child_count = len(self)
        if self.CAN_HAVE_TEXT and self.text:
            text = self.normalize_text(self.text)
            if self.STRIP:
                text = text.lstrip()
                if not child_count:
                    text = text.rstrip()
            builder.push_text(text)
        for i, child in enumerate(self):
            if isinstance(child, WLElement):
                getattr(child, build_method)(builder)
            if self.CAN_HAVE_TEXT and child.tail:
                text = self.normalize_text(child.tail)
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
        return attr
        
    def html_build(self, builder):
        if self.HTML_SECTION:
            builder.start_element(
                'a', {"name": "f18", "class": "target"}
            )
            builder.push_text(" ")
            builder.end_element()

            builder.start_element(
                "a", {"href": "#f18", "class": "anchor"}
            )
            builder.push_text("18")
            builder.end_element()
        

        if self.HTML_TAG:
            builder.start_element(
                self.HTML_TAG,
                self.get_html_attr(builder),
            )

        if self.HTML_SECTION:
            builder.start_element(
                "a", {"name": "sec34"}
            )
            builder.end_element()

        self._html_build_inner(builder)
        if self.HTML_TAG:
            builder.end_element()

    def sanitize(self):
        # TODO: Remove insanity here.
        for e in self:
            if isinstance(e, WLElement):
                e.sanitize()
