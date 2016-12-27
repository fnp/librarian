# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import os
import re
import urllib
from copy import deepcopy
from mimetypes import guess_type
from tempfile import NamedTemporaryFile
import zipfile
from urllib2 import urlopen

from lxml import etree
from librarian import OPFNS, NCXNS, XHTMLNS, DCNS, BuildError
from librarian import core
from librarian.formats import Format
from librarian.formats.cover.evens import EvensCover
from librarian.output import OutputFile
from librarian.renderers import Register, TreeRenderer, UnknownElement
from librarian.utils import Context, get_resource, extend_element


class EpubFormat(Format):
    format_name = 'EPUB'
    format_ext = 'epub'

    cover = EvensCover
    renderers = Register()

    def __init__(self, doc, cover=None, with_fonts=True):
        super(EpubFormat, self).__init__(doc)
        self.with_fonts = with_fonts
        if cover is not None:
            self.cover = cover

    def dc(self, tag):
        return self.doc.meta.get_one(DCNS(tag))

    def build(self, ctx=None):

        def add_file(url, file_id):
            filename = url.rsplit('/', 1)[1]
            if url.startswith('file://'):
                url = ctx.files_path + urllib.quote(url[7:])
            if url.startswith('/'):
                url = 'http://milpeer.eu' + url
            file_content = urlopen(url).read()
            zip.writestr(os.path.join('OPS', filename), file_content)
            manifest.append(etree.fromstring(
                '<item id="%s" href="%s" media-type="%s" />' % (file_id, filename, guess_type(url)[0])))

        opf = etree.parse(get_resource('formats/epub/res/content.opf'))
        manifest = opf.find(OPFNS('manifest'))
        guide = opf.find(OPFNS('guide'))
        spine = opf.find(OPFNS('spine'))

        author = ", ". join(self.doc.meta.get(DCNS('creator')) or [])
        title = self.doc.meta.title()
        opf.find('.//' + DCNS('creator')).text = author
        opf.find('.//' + DCNS('title')).text = title

        output_file = NamedTemporaryFile(prefix='librarian', suffix='.epub', delete=False)
        zip = zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED)

        mime = zipfile.ZipInfo()
        mime.filename = 'mimetype'
        mime.compress_type = zipfile.ZIP_STORED
        mime.extra = ''
        zip.writestr(mime, 'application/epub+zip')
        zip.writestr('META-INF/container.xml', '<?xml version="1.0" ?><container version="1.0" '
                     'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                     '<rootfiles><rootfile full-path="OPS/content.opf" '
                     'media-type="application/oebps-package+xml" />'
                     '</rootfiles></container>')

        toc_file = etree.fromstring('<?xml version="1.0" encoding="utf-8"?><!DOCTYPE ncx PUBLIC '
                                    '"-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">'
                                    '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" xml:lang="pl" '
                                    'version="2005-1"><head></head><docTitle></docTitle><navMap>'
                                    '</navMap></ncx>')
        # nav_map = toc_file[-1]

        if self.cover is not None:
            # cover_image = self.doc.meta.get(DCNS('relation.coverimage.url'))[0]
            cover = self.cover(self.doc)
            cover.set_images(ctx)
            cover_output = cover.build()
            cover_name = 'cover.%s' % cover.format_ext
            zip.writestr(os.path.join('OPS', cover_name), cover_output.get_string())
            del cover_output

            cover_tree = etree.parse(get_resource('formats/epub/res/cover.html'))
            cover_tree.find('//' + XHTMLNS('img')).set('src', cover_name)
            zip.writestr('OPS/cover.html', etree.tostring(
                            cover_tree, method="html", pretty_print=True))

            if cover.uses_dc_cover:
                if self.doc.meta.get_one('cover_by'):
                    self.doc.edoc.getroot().set('data-cover-by', self.doc.meta.get_one('cover_by'))
                if self.doc.meta.get_one('cover_source'):
                    self.doc.edoc.getroot().set('data-cover-source', self.doc.meta.get_one('cover_source'))

            manifest.append(etree.fromstring(
                '<item id="cover" href="cover.html" media-type="application/xhtml+xml" />'))
            manifest.append(etree.fromstring(
                '<item id="cover-image" href="%s" media-type="%s" />' % (cover_name, cover.mime_type())))
            spine.insert(0, etree.fromstring('<itemref idref="cover" linear="no" />'))
            opf.getroot()[0].append(etree.fromstring('<meta name="cover" content="cover-image"/>'))
            guide.append(etree.fromstring('<reference href="cover.html" type="cover" title="Okładka"/>'))

        if not ctx:
            ctx = Context(format=self)
        else:
            ctx.format = self
        ctx.toc = TOC()
        ctx.toc_level = 0
        ctx.footnotes = Footnotes()
        ctx.images = []
        ctx.part_no = 0

        wrap_tmpl = etree.parse(get_resource('formats/epub/res/chapter.html'))
        for e in self.render(self.doc.edoc.getroot(), ctx):
            if not len(e) and not (e.text and e.text.strip()):
                continue
            wrap = deepcopy(wrap_tmpl)
            extend_element(wrap.find('//*[@id="book-text"]'), e)

            partstr = 'part%d' % int(e.get('part_no'))
            manifest.append(manifest.makeelement(OPFNS('item'), attrib={
                                 'id': partstr,
                                 'href': partstr + ".html",
                                 'media-type': 'application/xhtml+xml',
                             }))
            spine.append(spine.makeelement(OPFNS('itemref'), attrib={
                        'idref': partstr,
                    }))
            zip.writestr('OPS/%s.html' % partstr, etree.tostring(wrap, method='html'))

        for i, url in enumerate(ctx.images):
            add_file(url, 'image%s' % i)

        if len(ctx.footnotes.output):
            ctx.toc.add("Przypisy", "footnotes.html")
            manifest.append(etree.Element(
                OPFNS('item'), id='footnotes', href='footnotes.html',
                **{'media-type': "application/xhtml+xml"}))
            spine.append(etree.Element('itemref', idref='footnotes'))
            wrap = etree.parse(get_resource('formats/epub/res/footnotes.html'))
            extend_element(wrap.find('//*[@id="footnotes"]'), ctx.footnotes.output)
            
            # chars = chars.union(used_chars(html_tree.getroot()))
            zip.writestr('OPS/footnotes.html', etree.tostring(
                                wrap, method="html", pretty_print=True))

        footer_text = [
            'Information about the resource',
            'Publisher: %s' % self.dc('publisher'),
            'Rights: %s' % self.dc('rights'),
            'Intended audience: %s' % self.dc('audience'),
            self.dc('description'),
            'Resource prepared using MIL/PEER editing platform.',
            'Source available at %s' % ctx.source_url,
        ]
        footer_wrap = deepcopy(wrap_tmpl)
        footer_body = footer_wrap.find('//*[@id="book-text"]')
        for line in footer_text:
            footer_line = etree.Element('p')
            footer_line.text = line
            footer_body.append(footer_line)
        manifest.append(manifest.makeelement(OPFNS('item'), attrib={
            'id': 'footer',
            'href': "footer.html",
            'media-type': 'application/xhtml+xml',
        }))
        spine.append(spine.makeelement(OPFNS('itemref'), attrib={
            'idref': 'footer',
        }))
        zip.writestr('OPS/footer.html', etree.tostring(footer_wrap, method='html'))

        zip.writestr('OPS/content.opf', etree.tostring(opf, pretty_print=True))
        ctx.toc.render(toc_file[-1])
        zip.writestr('OPS/toc.ncx', etree.tostring(toc_file, pretty_print=True))
        zip.close()
        return OutputFile.from_filename(output_file.name)

    def render(self, element, ctx):
        return self.renderers.get_for(element).render(element, ctx)


# Helpers

class EpubRenderer(TreeRenderer):
    """ Renders insides as XML in a <_/> container. """
    def container(self, ctx):
        root, inner = super(EpubRenderer, self).container()
        root.set("part_no", str(ctx.part_no))
        return root, inner

    def render(self, element, ctx):
        subctx = self.subcontext(element, ctx)
        wrapper, inside = self.container(ctx)
        if element.text:
            extend_element(inside, self.render_text(element.text, ctx))
        for child in element:
            try:
                child_renderer = ctx.format.renderers.get_for(child)
            except UnknownElement:
                continue
            else:
                if getattr(child_renderer, 'epub_separate', False):
                    yield wrapper
                    ctx.part_no += 1
                    for child_part in child_renderer.render(child, subctx):
                        yield child_part
                    wrapper, inside = self.container(ctx)
                else:
                    child_parts = list(child_renderer.render(child, subctx))
                    extend_element(inside, child_parts[0])
                    if len(child_parts) > 1:
                        yield wrapper
                        for child_part in child_parts[1:-1]:
                            yield child_part
                        wrapper, inside = self.container(ctx)
                        extend_element(inside, child_parts[-1])
            finally:
                if child.tail:
                    extend_element(inside, self.render_text(child.tail, ctx))
        yield wrapper


class NaturalText(EpubRenderer):
    def render_text(self, text, ctx):
        root, inner = self.text_container()
        chunks = re.split('(?<=\s\w) ', text)
        inner.text = chunks[0]
        for chunk in chunks[1:]:
            x = etree.Entity("nbsp")
            x.tail = chunk
            inner.append(x)
        return root


class Silent(EpubRenderer):
    def render_text(self, text, ctx):
        root, inner = self.text_container()
        return root


class Footnotes(object):
    def __init__(self):
        self.counter = 0
        self.output = etree.Element("_")

    def append(self, items):
        self.counter += 1
        e = etree.Element(
            "a", href="part%d.html#footnote-anchor-%d" % (int(items[0].get('part_no')), self.counter),
            id="footnote-%d" % self.counter,
            style="float:left;margin-right:1em")
        e.text = "[%d]" % self.counter
        e.tail = " "
        self.output.append(e)
        for item in items:
            extend_element(self.output, item)
        anchor = etree.Element(
            "a", href="footnotes.html#footnote-%d" % self.counter, id="footnote-anchor-%d" % self.counter)
        anchor.text = "[%d]" % self.counter
        return anchor


class TOC(object):
    def __init__(self, title=None, href="", root=None):
        if root is None:
            self.counter = 0
            self.root = self
        else:
            self.root = root
        self.children = []
        self.title = title
        self.href = href.format(counter=self.root.counter)
        self.number = self.root.counter
        self.root.counter += 1

    def add(self, title, href):
        subtoc = type(self)(title, href, root=self.root)
        self.children.append(subtoc)
        return subtoc

    def render(self, nav_map):
        for child in self.children:
            nav_point = etree.Element(NCXNS('navPoint'))
            nav_point.set('id', 'NavPoint-%d' % child.number)
            nav_point.set('playOrder', str(child.number))

            nav_label = etree.Element(NCXNS('navLabel'))
            text = etree.Element(NCXNS('text'))
            text.text = child.title
            nav_label.append(text)
            nav_point.append(nav_label)

            content = etree.Element(NCXNS('content'))
            content.set('src', child.href)
            nav_point.append(content)
            nav_map.append(nav_point)
            child.render(nav_point)


# Renderers

class AsideR(NaturalText):
    def render(self, element, ctx):
        outputs = list(super(AsideR, self).render(element, ctx))
        anchor = ctx.footnotes.append(outputs)
        wrapper, inside = self.text_container()  # etree.Element('_', part_no=str(ctx.part_no))
        inside.append(anchor)
        yield wrapper
EpubFormat.renderers.register(core.Aside, None, AsideR('div'))

EpubFormat.renderers.register(core.Aside, 'comment', Silent())


class DivR(NaturalText):
    def container(self, ctx):
        root, inner = super(DivR, self).container(ctx)
        if getattr(ctx, 'inline', False):
            inner.tag = 'span'
            inner.set('style', 'display: block;')
        return root, inner
EpubFormat.renderers.register(core.Div, None, DivR('div'))
EpubFormat.renderers.register(core.Div, 'p', NaturalText('p'))

EpubFormat.renderers.register(core.Div, 'list', NaturalText('ul'))
EpubFormat.renderers.register(core.Div, 'list.enum', NaturalText('ol'))
EpubFormat.renderers.register(core.Div, 'item', NaturalText('li'))
EpubFormat.renderers.register(core.Span, 'item', NaturalText('li'))


class DivImageR(EpubRenderer):
    def render(self, element, ctx):
        src = element.attrib.get('src', '')
        ctx.images.append(src)
        if '/' not in src:
            raise BuildError('Bad image URL')
        src = src.rsplit('/', 1)[1]
        return super(DivImageR, self).render(element, Context(ctx, src=src))

    def container(self, ctx):
        root, inner = super(DivImageR, self).container(ctx)
        src = getattr(ctx, 'src', '')
        inner.set('src', src)
        # inner.set('style', 'display: block; width: 60%; margin: 3em auto')
        return root, inner
EpubFormat.renderers.register(core.Div, 'img', DivImageR('img'))


class DivVideoR(Silent):
    def render(self, element, ctx):
        src = 'https://www.youtube.com/watch?v=%s' % element.attrib.get('videoid', '')
        return super(DivVideoR, self).render(element, Context(ctx, src=src))

    def container(self, ctx):
        root, inner = super(DivVideoR, self).container(ctx)
        src = getattr(ctx, 'src', '')
        link = etree.Element('a', {'href': src})
        link.text = src
        inner.append(link)
        return root, inner
EpubFormat.renderers.register(core.Div, 'video', DivVideoR('p'))


class HeaderR(NaturalText):
    def subcontext(self, element, ctx):
        return Context(ctx, inline=True)
EpubFormat.renderers.register(core.Header, None, HeaderR('h1'))


class SectionR(NaturalText):
    epub_separate = True

    def render(self, element, ctx):
        # Add 'poczatek'?
        if element.getparent() is not None:
            tocitem = ctx.toc.add(element.meta.title(), 'part%d.html' % ctx.part_no)
            ctx = Context(ctx, toc=tocitem)
        return super(SectionR, self).render(element, ctx)
EpubFormat.renderers.register(core.Section, None, SectionR())


class SpanR(NaturalText):
    pass
EpubFormat.renderers.register(core.Span, None, SpanR('span'))
EpubFormat.renderers.register(core.Span, 'cite', SpanR('i'))
EpubFormat.renderers.register(core.Span, 'emp', SpanR('b'))
EpubFormat.renderers.register(core.Span, 'emph', SpanR('i'))


class SpanLink(EpubRenderer):
    def render(self, element, ctx):
        parts = super(SpanLink, self).render(element, ctx)
        for part in parts:
            src = element.attrib.get('href', '')
            if src.startswith('file://'):
                src = ctx.files_path + src[7:]
            part[0].attrib['href'] = src
            yield part
EpubFormat.renderers.register(core.Span, 'link', SpanLink('a'))
