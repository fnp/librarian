# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from lxml import etree
from . import UnicodeException
from .utils import extend_element


class UnknownElement(UnicodeException):
    pass


class Renderer(object):
    """ Renders an element in a context to some kind of container. """
    def render(self, element, ctx):
        """ Renders the element in the context. """
        raise NotImplemented

    def render_text(self, text, ctx):
        """ Renders the text in the context. """
        raise NotImplemented


class TreeRenderer(Renderer):
    """ Renders insides as XML in a <_/> container. """
    root_name = "_"

    def __init__(self, tag_name=None, attrib=None):
        self.tag_name = tag_name
        self.attrib = attrib or {}

    def container(self):
        root = etree.Element(self.root_name)
        if self.tag_name:
            inner = etree.Element(self.tag_name, **self.attrib)
            root.append(inner)
            return root, inner
        else:
            return root, root

    def text_container(self):
        root = etree.Element(self.root_name)
        return root, root

    def subcontext(self, element, ctx):
        return ctx

    def get_insides(self, element, ctx):
        subctx = self.subcontext(element, ctx)
        if element.text:
            yield self.render_text(element.text, ctx)
        for child in element:
            try:
                yield ctx.format.render(child, subctx)
            except UnknownElement:
                pass
            if child.tail:
                yield self.render_text(child.tail, ctx)

    def render(self, element, ctx):
        root, inner = self.container()
        for inside in self.get_insides(element, ctx):
            extend_element(inner, inside)
        return root

    def render_text(self, text, ctx):
        root, inner = self.text_container()
        inner.text = text
        return root


class Register(object):
    """ Class-renderer register.

    >>> from librarian.core import Div
    >>> renderer = Renderer()
    >>> reg = Register()
    >>> reg.register(Div, 'a.b', renderer)
    >>> reg.get(Div, 'a.b.c') is renderer
    True

    """
    def __init__(self):
        self.classes = {}

    def register(self, tag, klass, renderer):
        self.classes[tag, klass] = renderer

    def get(self, tag, klass=None):
        while klass:
            try:
                return self.classes[tag, klass]
            except KeyError:
                try:
                    klass = klass.rsplit('.', 1)[-2]
                except IndexError:
                    klass = None
        try:
            return self.classes[tag, None]
        except KeyError:
            raise UnknownElement(tag)

    def get_for(self, element):
        return self.get(type(element), element.get('class'))
