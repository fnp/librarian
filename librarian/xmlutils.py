# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from lxml import etree
from collections import defaultdict


class Xmill(object):
    """Transforms XML to some text.
    Used instead of XSLT which is difficult and cumbersome.

    """
    def __init__(self, options=None):
        self._options = []
        if options:
            self._options.append(options)
        self.text_filters = []

    def register_text_filter(self, fun):
        self.text_filters.append(fun)

    def filter_text(self, text):
        for flt in self.text_filters:
            if text is None:
                return None
            text = flt(text)
        return text

    def generate(self, document):
        """Generate text from node using handlers defined in class."""
        output = self._handle_element(document)
        return u''.join([x for x in flatten(output) if x is not None])

    @property
    def options(self):
        """Returnes merged scoped options for current node.
        """
        # Here we can see how a decision not to return the modified map
        # leads to a need for a hack.
        return reduce(lambda a, b: a.update(b) or a, self._options, defaultdict(lambda: None))

    @options.setter
    def options(self, opts):
        """Sets options overrides for current and child nodes
        """
        self._options.append(opts)


    def _handle_for_element(self, element):
        ns = None
        tagname = None
#        from nose.tools import set_trace

        if element.tag[0] == '{':
            for nshort, nhref in element.nsmap.items():
                try:
                    if element.tag.index('{%s}' % nhref) == 0:
                        ns = nshort
                        tagname  = element.tag[len('{%s}' % nhref):]
                        break
                except ValueError:
                    pass
            if not ns:
                raise ValueError("Strange ns for tag: %s, nsmap: %s" %
                                 (element.tag, element.nsmap))
        else:
            tagname = element.tag

        if ns:
            meth_name = "handle_%s__%s" % (ns, tagname)
        else:
            meth_name = "handle_%s" % (tagname,)

        handler = getattr(self, meth_name, None)
        return handler

    def next(self, element):
        if len(element):
            return element[0]

        while True:
            sibling = element.getnext()
            if sibling is not None: return sibling  # found a new branch to dig into
            element = element.getparent()
            if element is None: return None  # end of tree

    def _handle_element(self, element):
        if isinstance(element, etree._Comment): return None
        
        handler = self._handle_for_element(element)
        # How many scopes
        try:
            options_scopes = len(self._options)

            if handler is None:
                pre = [self.filter_text(element.text)]
                post = [self.filter_text(element.tail)]
            else:
                vals = handler(element)
                # depending on number of returned values, vals can be None, a value, or a tuple.
                # how poorly designed is that? 9 lines below are needed just to unpack this.
                if vals is None:
                    return [self.filter_text(element.tail)]
                else:
                    if not isinstance(vals, tuple):
                        return [vals, self.filter_text(element.tail)]
                    else:
                        pre = [vals[0], self.filter_text(element.text)]
                        post = [vals[1], self.filter_text(element.tail)]

            out = pre + [self._handle_element(child) for child in element] + post
        finally:
            # clean up option scopes if necessary
            self._options = self._options[0:options_scopes]
        return out


def tag_open_close(name_, classes_=None, **attrs):
    u"""Creates tag beginning and end.
    
    >>> tag_open_close("a", "klass", x=u"ą<")
    (u'<a x="\\u0105&lt;" class="klass">', u'</a>')

    """
    if classes_:
        if isinstance(classes_, (tuple, list)): classes_ = ' '.join(classes_)
        attrs['class'] = classes_

    e = etree.Element(name_)
    e.text = " "
    for k, v in attrs.items():
        e.attrib[k] = v
    pre, post = etree.tostring(e, encoding=unicode).split(u"> <")
    return pre + u">", u"<" + post

def tag(name_, classes_=None, **attrs):
    """Returns a handler which wraps node contents in tag `name', with class attribute
    set to `classes' and other attributes according to keyword paramters
    """
    def _hnd(self, element):
        return tag_open_close(name_, classes_, **attrs)
    return _hnd


def tagged(name, classes=None, **attrs):
    """Handler decorator which wraps handler output in tag `name', with class attribute
    set to `classes' and other attributes according to keyword paramters
    """
    if classes:
        if isinstance(classes, (tuple,list)): classes = ' '.join(classes)
        attrs['class'] = classes
    a = ''.join([' %s="%s"' % (k,v) for (k,v) in attrs.items()])
    def _decor(f):
        def _wrap(self, element):
            r = f(self, element)
            if r is None: return

            prepend = "<%s%s>" % (name, a)
            append = "</%s>" % name

            if isinstance(r, tuple):
                return prepend + r[0], r[1] + append
            return prepend + r + append
        return _wrap
    return _decor


def ifoption(**options):
    """Decorator which enables node only when options are set
    """
    def _decor(f):
        def _handler(self, *args, **kw):
            opts = self.options
            for k, v in options.items():
                if opts[k] != v:
                    return
            return f(self, *args, **kw)
        return _handler
    return _decor

def flatten(l, ltypes=(list, tuple)):
    """flatten function from BasicPropery/BasicTypes package
    """
    ltype = type(l)
    l = list(l)
    i = 0
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)
