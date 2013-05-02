# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from lxml import etree
from librarian import DCNS, SSTNS


def text_value(meta):
    """ Finds out the text value of metadata element.
    
    >>> p = Person()
    >>> p.text = u"Czajka, Radek"
    >>> print text_value(p)
    Radek Czajka

    """
    if hasattr(meta, 'text_value'):
        return meta.text_value()
    else:
        return meta.text


class Metadata(etree.ElementBase):
    @classmethod
    def about(cls, element):
        meta = cls()
        meta._about = element
        return meta

    def get_about(self):
        if hasattr(self, '_about'):
            return self._about
        else:
            return self.getparent()

    def get(self, key, inherit=True):
        """ Finds metadata by its element name. """
        values = self.findall(key)
        if values:
            return [text_value(v) for v in values]
        elif inherit and self.get_about().getparent() is not None:
            return self.get_about().getparent().meta.get(key)
        elif inherit and hasattr(self.get_about(), 'meta_context'):
            return self.get_about().meta_context.get(key)
        else:
            return []

    def get_one(self, *args, **kwargs):
        values = self.get(*args, **kwargs)
        if values:
            return values[0]
        else:
            return None
        

    # Specials.

    def author(self):
        try:
            return unicode(self.get(DCNS('creator'))[0])
        except IndexError:
            return u""

    def slug(self):
        try:
            return self.get(DCNS('identifier'))[0].slug()
        except IndexError:
            return None

    def title(self):
        dc_title = self.get(DCNS('title'), inherit=False)
        if dc_title:
            return unicode(dc_title[0])
        else:
            header = self.get_about().find(SSTNS('header'))
            if header is not None:
                # FIXME: This should be a simple text representation
                return header.text
            else:
                return u""


class MetaItem(etree.ElementBase):
    pass


class Person(MetaItem):
    def text_value(self):
        return u" ".join(p.strip() for p in reversed(self.text.rsplit(u',', 1)))


class Identifier(MetaItem):
    def slug(self):
        return self.text.rstrip('/').rsplit('/', 1)[-1]
