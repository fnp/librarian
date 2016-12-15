# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import os


class Context(object):
    """ Processing context.
    
    >>> ctx = Context(a=1)
    >>> subctx = Context(ctx, a=2)
    >>> ctx.b = 3
    >>> print subctx.a, subctx.b
    2 3

    """
    def __init__(self, _upctx=None, **initial):
        object.__setattr__(self, '_upctx', _upctx)
        object.__setattr__(self, '_data', initial or {})

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        elif self._upctx is not None:
            return getattr(self._upctx, name)
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (type(self), name))

    def __setattr__(self, name, value):
        try:
            self.try_setattr(name, value)
        except ValueError:
            self._data[name] = value

    def try_setattr(self, name, value):
        if name in self._data:
            self._data[name] = value
        elif self._upctx is not None:
            self._upctx.try_setattr(name, value)
        else:
            raise ValueError


class XMLNamespace(object):
    """A handy structure to repsent names in an XML namespace."""
    def __init__(self, uri):
        self.uri = uri

    def __call__(self, tag):
        return '{%s}%s' % (self.uri, tag)

    def __contains__(self, tag):
        return tag.startswith('{' + str(self) + '}')

    def __repr__(self):
        return 'XMLNamespace(%r)' % self.uri

    def __str__(self):
        return '%s' % self.uri


def extend_element(container, element=None, text=None):
    """ Extends XML element with another one's contents.

    Differs from etree.Element.extend by taking the text into account.

    >>> from lxml import etree
    >>> container = etree.fromstring("<A><B/></A>")
    >>> element = etree.fromstring("<_>a<b/>c</_>")
    >>> extend_element(container, element)
    >>> print etree.tostring(container)
    <A><B/>a<b/>c</A>

    """
    add_text = (text or "") + (element.text or "" if element is not None else "")
    if add_text:
        if len(container):
            container[-1].tail = (container[-1].tail or "") + add_text
        else:
            container.text = (container.text or "") + add_text
    if element is not None:
        container.extend(element)


def get_resource(path):
    return os.path.join(os.path.dirname(__file__), path)
