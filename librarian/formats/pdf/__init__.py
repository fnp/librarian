# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import os
import shutil
from subprocess import call, PIPE
from tempfile import NamedTemporaryFile, mkdtemp
from lxml import etree
from urllib import urlretrieve
from StringIO import StringIO
from Texml.processor import process
from librarian import DCNS, XMLNamespace, BuildError
from librarian.formats import Format
from librarian.output import OutputFile
from librarian.renderers import Register, TreeRenderer
from librarian.utils import Context, get_resource
from librarian import core
from PIL import Image
from ..html import Silent


TexmlNS = XMLNamespace('http://getfo.sourceforge.net/texml/ns1')


def texml_cmd(name, *parms, **kwargs):
    cmd = etree.Element(TexmlNS('cmd'), name=name)
    for opt in kwargs.get('opts', []):
        etree.SubElement(cmd, TexmlNS('opt')).text = opt
    for parm in parms:
        etree.SubElement(cmd, TexmlNS('parm')).text = parm
    return cmd


class PdfFormat(Format):
    format_name = 'PDF'
    format_ext = 'pdf'
    tex_passes = 1
    style = get_resource('formats/pdf/res/default.sty')

    local_packages = [
        get_resource('formats/pdf/res/coverimage.sty'),
        get_resource('formats/pdf/res/insertimage.sty'),
    ]

    renderers = Register()

    def retrieve_file(self, url, save_as):
        # TODO: local sheme
        return False

    def add_file(self, ctx, filename, url=None, path=None, image=False):
        from subprocess import call
        if not url and not path:
            raise BuildError('No URL or path for image')
        save_as = os.path.join(ctx.workdir, filename)
        if path is not None:
            ext = path.rsplit('.', 1)[-1]
            if image:
                if ext == 'gif':
                    call(['convert', path, save_as])
                else:
                    # JPEGs with bad density will break LaTeX with 'Dimension too large'.
                    call(['convert', '-units', 'PixelsPerInch', path, '-density', '300', save_as + '_.' + ext])
                    shutil.move(save_as + '_.' + ext, save_as)
            else:
                shutil.copy(path, save_as)
        elif not self.retrieve_file(url, save_as):
            if url.startswith('file://'):
                url = ctx.files_path + url[7:]

            if url.startswith('/'):
                url = 'http://milpeer.eu' + url

            if '.' not in url:
                raise BuildError('Linked file without extension: %s' % url)
            ext = url.rsplit('.', 1)[-1]
            if image:
                urlretrieve(url, save_as + '_.' + ext)
                if ext == 'gif':
                    call(['convert', save_as + '_.' + ext, save_as])
                else:
                    # JPEGs with bad density will break LaTeX with 'Dimension too large'.
                    r = call(['convert', '-units', 'PixelsPerInch', save_as + '_.' + ext, '-density', '300',
                              save_as + '_2.' + ext])
                    if r:
                        shutil.move(save_as + '_.' + ext, save_as)
                    else:
                        shutil.move(save_as + '_2.' + ext, save_as)
            else:
                urlretrieve(url, save_as)

    def get_file(self, ctx, filename):
        return os.path.join(ctx.workdir, filename)

    def get_texml(self, build_ctx):
        t = etree.Element(TexmlNS('TeXML'))

        self.add_file(build_ctx, 'wl.cls', path=get_resource('formats/pdf/res/wl.cls'))
        t.append(texml_cmd("documentclass", "wl"))

        # global packages
        self.add_file(build_ctx, 'style.sty', path=self.style)
        t.append(texml_cmd("usepackage", "style"))
        t.append(texml_cmd("usepackage", "hyphenat"))

        # local packages
        for i, package in enumerate(self.local_packages):
            self.add_file(build_ctx, "librarianlocalpackage%s.sty" % i, path=package)
            t.append(texml_cmd("usepackage", "librarianlocalpackage%s" % i))

        author = ", ". join(self.doc.meta.get(DCNS('creator')) or '')
        title = self.doc.meta.title()
        t.append(texml_cmd("author", author))
        t.append(texml_cmd("title", title))

        doc = etree.SubElement(t, TexmlNS('env'), name="document")

        # Wielkości!
        title_field = texml_cmd("titlefield", "")
        doc.append(title_field)
        grp = title_field[0]
        grp.append(texml_cmd("raggedright"))
        grp.append(texml_cmd("vfill"))
        if author:
            p = texml_cmd("par", "")
            grp.append(p)
            p[0].append(texml_cmd("Large"))
            p[0].append(texml_cmd("noindent"))
            p[0].append(texml_cmd("nohyphens", author))
            p[0].append(texml_cmd("vspace", "1em"))
            # p[0][-1].tail = author
        if title:
            p = texml_cmd("par", "")
            grp.append(p)
            p[0].append(texml_cmd("Huge"))
            p[0].append(texml_cmd("noindent"))
            p[0].append(texml_cmd("nohyphens", title))
            # p[0][-1].tail = title

        # IOFile probably would be better
        cover_logo_url = getattr(build_ctx, 'cover_logo', None)
        # TEST
        # TODO: convert
        # cover_logo_url = 'http://milpeer.mdrn.pl/media/dynamic/people/logo/nowoczesnapolska.org.pl.png'
        if cover_logo_url:
            self.add_file(build_ctx, 'coverlogo.png', cover_logo_url, image=True)
            size = Image.open(self.get_file(build_ctx, 'coverlogo.png')).size
            doc.append(texml_cmd("toplogo", 'coverlogo.png', "%fcm" % (2.0 * size[0] / size[1]), "2cm"))

        doc.append(texml_cmd("vspace", "2em"))

        ctx = Context(build_ctx, format=self, img=1)
        root = self.doc.edoc.getroot()
        root.remove(root[1])
        doc.extend(self.render(root, ctx))

        # Redakcyjna na końcu.
        doc.append(texml_cmd("section*", "Information about the resource"))
        doc.append(texml_cmd("vspace", "1em"))

        for m, f, multiple in (
                ('Publisher: ', DCNS('publisher'), False),
                ('Rights: ', DCNS('rights'), False),
                ('', DCNS('description'), False)):
            if multiple:
                v = ', '.join(self.doc.meta.get(f))
            else:
                v = self.doc.meta.get_one(f)
            if v:
                e = texml_cmd("par", "")
                e[0].append(texml_cmd("noindent"))
                e[0][0].tail = "%s%s" % (m, v)
                doc.append(e)
                doc.append(texml_cmd("vspace", "1em"))

        e = texml_cmd("par", "")
        e[0].append(texml_cmd("noindent"))
        e[0][0].tail = "Resource prepared using "
        e[0].append(texml_cmd("href", "http://milpeer.eu", "MIL/PEER"))
        e[0][-1].tail = " editing platform. "
        doc.append(e)

        source_url = getattr(build_ctx, 'source_url', None)
        # source_url = 'http://milpeer.mdrn.pl/documents/27/'
        if source_url:
            e = texml_cmd("par", "")
            doc.append(e)
            e[0].append(texml_cmd("noindent"))
            e[0][0].tail = "Source available at "
            e[0].append(texml_cmd("href", source_url, source_url))

        return t

    def get_tex_dir(self, ctx):
        ctx.workdir = mkdtemp('-wl2pdf')
        texml = self.get_texml(ctx)
        tex_path = os.path.join(ctx.workdir, 'doc.tex')
        with open(tex_path, 'w') as fout:
            # print etree.tostring(texml)
            process(StringIO(etree.tostring(texml)), fout, 'utf-8')

        # if self.save_tex:
        #     shutil.copy(tex_path, self.save_tex)

        # for sfile in ['wasysym.sty', 'uwasyvar.fd', 'uwasy.fd']:
        #     shutil.copy(get_resource(os.path.join('res/wasysym', sfile)), temp)
        return ctx.workdir

    def build(self, ctx=None, verbose=False):
        temp = self.get_tex_dir(ctx)
        tex_path = os.path.join(temp, 'doc.tex')
        try:
            cwd = os.getcwd()
        except OSError:
            cwd = None
        os.chdir(temp)

        if verbose:
            for i in range(self.tex_passes):
                p = call(['xelatex', tex_path])
        else:
            for i in range(self.tex_passes):
                p = call(['xelatex', '-interaction=batchmode', tex_path],
                         stdout=PIPE, stderr=PIPE)
        if p:
            # raise ParseError("Error parsing .tex file: %s" % tex_path)
            raise RuntimeError("Error parsing .tex file: %s" % tex_path)

        if cwd is not None:
            os.chdir(cwd)

        output_file = NamedTemporaryFile(prefix='librarian', suffix='.pdf', delete=False)
        pdf_path = os.path.join(temp, 'doc.pdf')
        shutil.move(pdf_path, output_file.name)
        shutil.rmtree(temp)
        os.system("ls -l " + output_file.name)
        return OutputFile.from_filename(output_file.name)
    
    def render(self, element, ctx):
        return self.renderers.get_for(element).render(element, ctx)


class CmdRenderer(TreeRenderer):
    def parms(self):
        return []

    def container(self):
        root = etree.Element(self.root_name)
        root.append(texml_cmd(self.tag_name, *(self.parms() + [""])))
        inner = root[0][-1]
        return root, inner


class EnvRenderer(TreeRenderer):
    def container(self):
        root = etree.Element(self.root_name)
        inner = etree.SubElement(root, 'env', name=self.tag_name)
        return root, inner


class GroupRenderer(CmdRenderer):
    def container(self):
        root = etree.Element(self.root_name)
        inner = etree.SubElement(root, 'group')
        if self.tag_name:
            inner.append(texml_cmd(self.tag_name, *(self.parms() + [""])))
        return root, inner


class SectionRenderer(CmdRenderer):
    def subcontext(self, element, ctx):
        # here?
        return Context(ctx, toc_level=getattr(ctx, 'toc_level', 1) + 2)

    def container(self):
        root = etree.Element(self.root_name)
        root.append(texml_cmd('pagebreak', opts=['1']))
        root.append(texml_cmd(self.tag_name, *(self.parms() + [""])))
        inner = root[1][0]
        return root, inner

PdfFormat.renderers.register(core.Section, None, SectionRenderer('par'))

# TODO: stopnie
PdfFormat.renderers.register(core.Header, None, CmdRenderer('section*'))

PdfFormat.renderers.register(core.Div, None, CmdRenderer('par'))


class ImgRenderer(CmdRenderer):
    def parms(self):
        return ["", ""]

    def render(self, element, ctx):
        root = super(ImgRenderer, self).render(element, ctx)
        url = element.get('src')
        nr = getattr(ctx, 'img', 0)
        ctx.img = nr + 1
        ctx.format.add_file(ctx, 'f%d.png' % nr, url, image=True)
        root[0][0].text = 'f%d.png' % nr
        try:
            size = Image.open(ctx.format.get_file(ctx, 'f%d.png' % nr)).size
        except IOError:  # not an image
            del root[0]
            return root
        root[0][1].text = '15cm'
        root[0][2].text = '%fcm' % (15.0 * size[1] / size[0])
        return root

PdfFormat.renderers.register(core.Div, 'img', ImgRenderer('insertimage'))


class VideoRenderer(CmdRenderer):
    def render(self, element, ctx):
        root = super(VideoRenderer, self).render(element, ctx)
        url = 'https://www.youtube.com/watch?v=%s' % element.attrib.get('videoid')
        link = texml_cmd('href', url, url)
        root[0][0].text = None
        root[0][0].append(link)
        return root

PdfFormat.renderers.register(core.Div, 'video', VideoRenderer('par'))


PdfFormat.renderers.register(core.Div, 'defined', CmdRenderer('textbf'))
PdfFormat.renderers.register(core.Div, 'item', CmdRenderer('item'))
PdfFormat.renderers.register(core.Span, 'item', CmdRenderer('item'))
PdfFormat.renderers.register(core.Div, 'list', EnvRenderer('itemize'))
PdfFormat.renderers.register(core.Div, 'list.enum', EnvRenderer('enumerate'))


PdfFormat.renderers.register(core.Span, None, TreeRenderer())
PdfFormat.renderers.register(core.Span, 'cite', CmdRenderer('emph'))
PdfFormat.renderers.register(core.Span, 'cite.code', CmdRenderer('texttt'))
PdfFormat.renderers.register(core.Span, 'emp', CmdRenderer('textbf'))
PdfFormat.renderers.register(core.Span, 'emph', CmdRenderer('emph'))


class SpanUri(CmdRenderer):
    def parms(self):
        return [""]

    def render(self, element, ctx):
        root = super(SpanUri, self).render(element, ctx)
        src = element.text
        if src.startswith('file://'):
            src = ctx.files_path + src[7:]
        root[0][0].text = src
        return root
PdfFormat.renderers.register(core.Span, 'uri', SpanUri('href'))


class SpanLink(CmdRenderer):
    def parms(self):
        return [""]

    def render(self, element, ctx):
        root = super(SpanLink, self).render(element, ctx)
        src = element.attrib.get('href', '')
        if src.startswith('file://'):
            src = ctx.files_path + src[7:]
        root[0][0].text = src
        return root
PdfFormat.renderers.register(core.Span, 'link', SpanLink('href'))


PdfFormat.renderers.register(core.Aside, None, TreeRenderer())
PdfFormat.renderers.register(core.Aside, 'editorial', CmdRenderer('editorialpage'))
PdfFormat.renderers.register(core.Aside, 'comment', Silent())
