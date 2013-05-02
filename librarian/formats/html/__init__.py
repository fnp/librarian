# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import re
from lxml import etree
from librarian.formats import Format
from librarian.output import OutputFile
from librarian.renderers import Register, TreeRenderer
from librarian.utils import Context, get_resource
from librarian import core


class HtmlFormat(Format):
    format_name = 'HTML'
    format_ext = 'html'

    renderers = Register()

    def __init__(self, doc, standalone=False):
        super(HtmlFormat, self).__init__(doc)
        self.standalone = standalone

    def build(self):
        if self.standalone:
            tmpl = get_resource("formats/html/res/html_standalone.html")
        else:
            tmpl = get_resource("formats/html/res/html.html")
        t = etree.parse(tmpl)

        ctx = Context(format=self)
        ctx.toc = TOC()
        ctx.toc_level = 0
        ctx.footnotes = Footnotes()

        if self.standalone:
            t.find('head/title').text = u"%s (%s)" % (self.doc.meta.title(), self.doc.meta.author())

        t.find('.//div[@id="content"]').extend(
            self.render(self.doc.edoc.getroot(), ctx))
        t.find('.//div[@id="toc"]').append(ctx.toc.render())
        t.find('.//div[@id="footnotes"]').extend(ctx.footnotes.output)

        return OutputFile.from_string(etree.tostring(
            t, encoding='utf-8', method="html"))

    def render(self, element, ctx):
        return self.renderers.get_for(element).render(element, ctx)


# Helpers

class NaturalText(TreeRenderer):
    def render_text(self, text, ctx):
        root, inner = self.text_container()
        chunks = re.split('(?<=\s\w) ', text)
        inner.text = chunks[0]
        for chunk in chunks[1:]:
            x = etree.Entity("nbsp")
            x.tail = chunk
            inner.append(x)
        return root


class LiteralText(TreeRenderer):
    pass


class Footnotes(object):
    def __init__(self):
        self.counter = 0
        self.output = etree.Element("_")

    def append(self, item):
        self.counter += 1
        e = etree.Element("a",
            href="#footnote-anchor-%d" % self.counter,
            id="footnote-%d" % self.counter,
            style="float:left;margin-right:1em")
        e.text = "[%d]" % self.counter
        e.tail = " "
        self.output.append(e)
        self.output.extend(item)
        anchor = etree.Element("a",
            id="footnote-anchor-%d" % self.counter,
            href="#footnote-%d" % self.counter)
        anchor.text = "[%d]" % self.counter
        return anchor


class TOC(object):
    def __init__(self):
        self.items = []
        self.counter = 0

    def add(self, title, level=0):
        self.counter += 1
        self.items.append((level, title, self.counter))
        return self.counter

    def render(self):
        out = etree.Element("ul", id="toc")
        curr_level = 0
        cursor = out
        for level, title, counter in self.items:
            while level > curr_level:
                ins = etree.Element("ul")
                cursor.append(ins)
                cursor = ins
                curr_level += 1
            while level < curr_level:
                cursor = cursor.getparent()
                curr_level -= 1
            ins = etree.Element("li")
            ins.append(etree.Element("a", href="#sect%d" % counter))
            ins[0].text = title
            cursor.append(ins)
        return out


# Renderers

HtmlFormat.renderers.register(core.Aside, None, NaturalText('aside'))

class AsideFootnote(NaturalText):
    def render(self, element, ctx):
        output = super(AsideFootnote, self).render(element, ctx)
        anchor = ctx.footnotes.append(output)
        root, inner = self.container()
        inner.append(anchor)
        return root
HtmlFormat.renderers.register(core.Aside, 'footnote', AsideFootnote())

       
HtmlFormat.renderers.register(core.Header, None, NaturalText('h1'))


HtmlFormat.renderers.register(core.Div, None, NaturalText('div'))
HtmlFormat.renderers.register(core.Div, 'item', NaturalText('li'))
HtmlFormat.renderers.register(core.Div, 'list', NaturalText('ul'))
HtmlFormat.renderers.register(core.Div, 'p', NaturalText('p'))


class Section(NaturalText):
    def subcontext(self, element, ctx):
        return Context(ctx, toc_level=ctx.toc_level + 1)

    def render(self, element, ctx):
        counter = ctx.toc.add(element.meta.title(), ctx.toc_level)
        root = super(Section, self).render(element, ctx)
        root[0].set("id", "sect%d" % counter)
        return root
HtmlFormat.renderers.register(core.Section, None, Section('section'))


HtmlFormat.renderers.register(core.Span, None, NaturalText('span'))
HtmlFormat.renderers.register(core.Span, 'cite', NaturalText('cite'))
HtmlFormat.renderers.register(core.Span, 'cite.code', LiteralText('code'))
HtmlFormat.renderers.register(core.Span, 'emph', NaturalText('em'))

class SpanUri(LiteralText):
    def render(self, element, ctx):
        root = super(SpanUri, self).render(element, ctx)
        root[0].attrib['href'] = element.text
        return root
HtmlFormat.renderers.register(core.Span, 'uri', SpanUri('a'))
