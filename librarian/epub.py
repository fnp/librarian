# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from __future__ import with_statement

import os
import os.path
import subprocess
from StringIO import StringIO
from copy import deepcopy
from lxml import etree
import zipfile
from tempfile import mkdtemp
from shutil import rmtree

import sys

from librarian import XMLNamespace, RDFNS, DCNS, WLNS, NCXNS, OPFNS, XHTMLNS, NoDublinCore
from librarian.dcparser import BookInfo

from librarian import functions, get_resource

functions.reg_person_name()


def inner_xml(node):
    """ returns node's text and children as a string

    >>> print inner_xml(etree.fromstring('<a>x<b>y</b>z</a>'))
    x<b>y</b>z
    """

    nt = node.text if node.text is not None else ''
    return ''.join([nt] + [etree.tostring(child) for child in node])

def set_inner_xml(node, text):
    """ sets node's text and children from a string

    >>> e = etree.fromstring('<a>b<b>x</b>x</a>')
    >>> set_inner_xml(e, 'x<b>y</b>z')
    >>> print etree.tostring(e)
    <a>x<b>y</b>z</a>
    """

    p = etree.fromstring('<x>%s</x>' % text)
    node.text = p.text
    node[:] = p[:]


def node_name(node):
    """ Find out a node's name

    >>> print node_name(etree.fromstring('<a>X<b>Y</b>Z</a>'))
    XYZ
    """

    tempnode = deepcopy(node)

    for p in ('pe', 'pa', 'pt', 'pr', 'motyw'):
        for e in tempnode.findall('.//%s' % p):
            t = e.tail
            e.clear()
            e.tail = t
    etree.strip_tags(tempnode, '*')
    return tempnode.text


def xslt(xml, sheet):
    if isinstance(xml, etree._Element):
        xml = etree.ElementTree(xml)
    with open(sheet) as xsltf:
        return xml.xslt(etree.parse(xsltf))


def replace_characters(node):
    def replace_chars(text):
        if text is None:
            return None
        return text.replace(u"\ufeff", u"")\
                   .replace("---", u"\u2014")\
                   .replace("--", u"\u2013")\
                   .replace(",,", u"\u201E")\
                   .replace('"', u"\u201D")\
                   .replace("'", u"\u2019")
    if node.tag in ('uwaga', 'extra'):
        t = node.tail
        node.clear()
        node.tail = t
    node.text = replace_chars(node.text)
    node.tail = replace_chars(node.tail)
    for child in node:
        replace_characters(child)


def find_annotations(annotations, source, part_no):
    for child in source:
        if child.tag in ('pe', 'pa', 'pt', 'pr'):
            annotation = deepcopy(child)
            number = str(len(annotations)+1)
            annotation.set('number', number)
            annotation.set('part', str(part_no))
            annotation.tail = ''
            annotations.append(annotation)
            tail = child.tail
            child.clear()
            child.tail = tail
            child.text = number
        if child.tag not in ('extra', 'uwaga'):
            find_annotations(annotations, child, part_no)


def replace_by_verse(tree):
    """ Find stanzas and create new verses in place of a '/' character """

    stanzas = tree.findall('.//' + WLNS('strofa'))
    for node in stanzas:
        for child_node in node:
            if child_node.tag in ('slowo_obce', 'wyroznienie'):
                foreign_verses = inner_xml(child_node).split('/\n')
                if len(foreign_verses) > 1:
                    new_foreign = ''
                    for foreign_verse in foreign_verses:
                        if foreign_verse.startswith('<wers'):
                            new_foreign += foreign_verse
                        else:
                            new_foreign += ''.join(('<wers_normalny>', foreign_verse, '</wers_normalny>'))
                    set_inner_xml(child_node, new_foreign)
        verses = inner_xml(node).split('/\n')
        if len(verses) > 1:
            modified_inner_xml = ''
            for verse in verses:
                if verse.startswith('<wers') or verse.startswith('<extra'):
                    modified_inner_xml += verse
                else:
                    modified_inner_xml += ''.join(('<wers_normalny>', verse, '</wers_normalny>'))
            set_inner_xml(node, modified_inner_xml)


def add_to_manifest(manifest, partno):
    """ Adds a node to the manifest section in content.opf file """

    partstr = 'part%d' % partno
    e = manifest.makeelement(OPFNS('item'), attrib={
                                 'id': partstr,
                                 'href': partstr + '.html',
                                 'media-type': 'application/xhtml+xml',
                             })
    manifest.append(e)


def add_to_spine(spine, partno):
    """ Adds a node to the spine section in content.opf file """

    e = spine.makeelement(OPFNS('itemref'), attrib={'idref': 'part%d' % partno});
    spine.append(e)


class TOC(object):
    def __init__(self, name=None, part_number=None):
        self.children = []
        self.name = name
        self.part_number = part_number
        self.sub_number = None

    def add(self, name, part_number, level=0, is_part=True):
        if level > 0 and self.children:
            return self.children[-1].add(name, part_number, level-1, is_part)
        else:
            t = TOC(name)
            t.part_number = part_number
            self.children.append(t)
            if not is_part:
                t.sub_number = len(self.children) + 1
                return t.sub_number

    def append(self, toc):
        self.children.append(toc)

    def extend(self, toc):
        self.children.extend(toc.children)

    def depth(self):
        if self.children:
            return max((c.depth() for c in self.children)) + 1
        else:
            return 0

    def write_to_xml(self, nav_map, counter):
        for child in self.children:
            nav_point = nav_map.makeelement(NCXNS('navPoint'))
            nav_point.set('id', 'NavPoint-%d' % counter)
            nav_point.set('playOrder', str(counter))

            nav_label = nav_map.makeelement(NCXNS('navLabel'))
            text = nav_map.makeelement(NCXNS('text'))
            text.text = child.name
            nav_label.append(text)
            nav_point.append(nav_label)

            content = nav_map.makeelement(NCXNS('content'))
            src = 'part%d.html' % child.part_number
            if child.sub_number is not None:
                src += '#sub%d' % child.sub_number
            content.set('src', src)
            nav_point.append(content)
            nav_map.append(nav_point)
            counter = child.write_to_xml(nav_point, counter + 1)
        return counter


def used_chars(element):
    """ Lists characters used in an ETree Element """
    chars = set((element.text or '') + (element.tail or ''))
    for child in element:
        chars = chars.union(used_chars(child))
    return chars


def chop(main_text):
    """ divide main content of the XML file into chunks """

    # prepare a container for each chunk
    part_xml = etree.Element('utwor')
    etree.SubElement(part_xml, 'master')
    main_xml_part = part_xml[0] # master

    last_node_part = False
    for one_part in main_text:
        name = one_part.tag
        if name == 'naglowek_czesc':
            yield part_xml
            last_node_part = True
            main_xml_part[:] = [deepcopy(one_part)]
        elif not last_node_part and name in ("naglowek_rozdzial", "naglowek_akt", "srodtytul"):
            yield part_xml
            main_xml_part[:] = [deepcopy(one_part)]
        else:
            main_xml_part.append(deepcopy(one_part))
            last_node_part = False
    yield part_xml


def transform_chunk(chunk_xml, chunk_no, annotations, empty=False, _empty_html_static=[]):
    """ transforms one chunk, returns a HTML string, a TOC object and a set of used characters """

    toc = TOC()
    for element in chunk_xml[0]:
        if element.tag in ("naglowek_czesc", "naglowek_rozdzial", "naglowek_akt", "srodtytul"):
            toc.add(node_name(element), chunk_no)
        elif element.tag in ('naglowek_podrozdzial', 'naglowek_scena'):
            subnumber = toc.add(node_name(element), chunk_no, level=1, is_part=False)
            element.set('sub', str(subnumber))
    if empty:
        if not _empty_html_static:
            _empty_html_static.append(open(get_resource('epub/emptyChunk.html')).read())
        chars = set()
        output_html = _empty_html_static[0]
    else:
        find_annotations(annotations, chunk_xml, chunk_no)
        replace_by_verse(chunk_xml)
        html_tree = xslt(chunk_xml, get_resource('epub/xsltScheme.xsl'))
        chars = used_chars(html_tree.getroot())
        output_html = etree.tostring(html_tree, method="html", pretty_print=True)
    return output_html, toc, chars


def transform(provider, slug=None, file_path=None, output_file=None, output_dir=None, make_dir=False, verbose=False,
              sample=None, cover=None, flags=None):
    """ produces a EPUB file

    provider: a DocProvider
    slug: slug of file to process, available by provider
    output_file: file-like object or path to output file
    output_dir: path to directory to save output file to; either this or output_file must be present
    make_dir: writes output to <output_dir>/<author>/<slug>.epub instead of <output_dir>/<slug>.epub
    sample=n: generate sample e-book (with at least n paragraphs)
    cover: a cover.Cover object
    flags: less-advertising,
    """

    def transform_file(input_xml, chunk_counter=1, first=True, sample=None):
        """ processes one input file and proceeds to its children """

        replace_characters(input_xml.getroot())

        children = [child.text for child in input_xml.findall('.//'+DCNS('relation.hasPart'))]

        # every input file will have a TOC entry,
        # pointing to starting chunk
        toc = TOC(node_name(input_xml.find('.//'+DCNS('title'))), chunk_counter)
        chars = set()
        if first:
            # write book title page
            html_tree = xslt(input_xml, get_resource('epub/xsltTitle.xsl'))
            chars = used_chars(html_tree.getroot())
            zip.writestr('OPS/title.html',
                 etree.tostring(html_tree, method="html", pretty_print=True))
        elif children:
            # write title page for every parent
            if sample is not None and sample <= 0:
                chars = set()
                html_string = open(get_resource('epub/emptyChunk.html')).read()
            else:
                html_tree = xslt(input_xml, get_resource('epub/xsltChunkTitle.xsl'))
                chars = used_chars(html_tree.getroot())
                html_string = etree.tostring(html_tree, method="html", pretty_print=True)
            zip.writestr('OPS/part%d.html' % chunk_counter, html_string)
            add_to_manifest(manifest, chunk_counter)
            add_to_spine(spine, chunk_counter)
            chunk_counter += 1

        if len(input_xml.getroot()) > 1:
            # rdf before style master
            main_text = input_xml.getroot()[1]
        else:
            # rdf in style master
            main_text = input_xml.getroot()[0]
            if main_text.tag == RDFNS('RDF'):
                main_text = None

        if main_text is not None:
            for chunk_xml in chop(main_text):
                empty = False
                if sample is not None:
                    if sample <= 0:
                        empty = True
                    else:
                        sample -= len(chunk_xml.xpath('//strofa|//akap|//akap_cd|//akap_dialog'))
                chunk_html, chunk_toc, chunk_chars = transform_chunk(chunk_xml, chunk_counter, annotations, empty)

                toc.extend(chunk_toc)
                chars = chars.union(chunk_chars)
                zip.writestr('OPS/part%d.html' % chunk_counter, chunk_html)
                add_to_manifest(manifest, chunk_counter)
                add_to_spine(spine, chunk_counter)
                chunk_counter += 1

        if children:
            for child in children:
                child_xml = etree.parse(provider.by_uri(child))
                child_toc, chunk_counter, chunk_chars, sample = transform_file(child_xml, chunk_counter, first=False, sample=sample)
                toc.append(child_toc)
                chars = chars.union(chunk_chars)

        return toc, chunk_counter, chars, sample

    # read metadata from the first file
    if file_path:
        if slug:
            raise ValueError('slug or file_path should be specified, not both')
        f = open(file_path, 'r')
        input_xml = etree.parse(f)
        f.close()
    else:
        if not slug:
            raise ValueError('either slug or file_path should be specified')
        input_xml = etree.parse(provider[slug])

    if flags:
        for flag in flags:
            input_xml.getroot().set(flag, 'yes')

    metadata = input_xml.find('.//'+RDFNS('Description'))
    if metadata is None:
        raise NoDublinCore('Document has no DublinCore - which is required.')
    book_info = BookInfo.from_element(input_xml)
    metadata = etree.ElementTree(metadata)

    # if output to dir, create the file
    if output_dir is not None:
        if make_dir:
            author = unicode(book_info.author)
            output_dir = os.path.join(output_dir, author)
            try:
                os.makedirs(output_dir)
            except OSError:
                pass
        if slug:
            output_file = open(os.path.join(output_dir, '%s.epub' % slug), 'w')
        else:
            output_file = open(os.path.join(output_dir, os.path.splitext(os.path.basename(file_path))[0] + '.epub'), 'w')

    zip = zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED)

    # write static elements
    mime = zipfile.ZipInfo()
    mime.filename = 'mimetype'
    mime.compress_type = zipfile.ZIP_STORED
    mime.extra = ''
    zip.writestr(mime, 'application/epub+zip')
    zip.writestr('META-INF/container.xml', '<?xml version="1.0" ?><container version="1.0" ' \
                       'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">' \
                       '<rootfiles><rootfile full-path="OPS/content.opf" ' \
                       'media-type="application/oebps-package+xml" />' \
                       '</rootfiles></container>')
    zip.write(get_resource('epub/style.css'), os.path.join('OPS', 'style.css'))
    zip.write(get_resource('res/wl-logo-small.png'), os.path.join('OPS', 'logo_wolnelektury.png'))
    zip.write(get_resource('res/jedenprocent.png'), os.path.join('OPS', 'jedenprocent.png'))

    opf = xslt(metadata, get_resource('epub/xsltContent.xsl'))
    manifest = opf.find('.//' + OPFNS('manifest'))
    spine = opf.find('.//' + OPFNS('spine'))

    if cover:
        cover_file = StringIO()
        c = cover(book_info.author.readable(), book_info.title)
        c.save(cover_file)
        c_name = 'cover.%s' % c.ext()
        zip.writestr(os.path.join('OPS', c_name), cover_file.getvalue())
        del cover_file

        cover_tree = etree.parse(get_resource('epub/cover.html'))
        cover_tree.find('//' + XHTMLNS('img')).set('src', c_name)
        zip.writestr('OPS/cover.html', etree.tostring(
                        cover_tree, method="html", pretty_print=True))

        manifest.append(etree.fromstring(
            '<item id="cover" href="cover.html" media-type="application/xhtml+xml" />'))
        manifest.append(etree.fromstring(
            '<item id="cover-image" href="%s" media-type="%s" />' % (c_name, c.mime_type())))
        spine.insert(0, etree.fromstring('<itemref idref="cover" />'))
        opf.getroot()[0].append(etree.fromstring('<meta name="cover" content="cover-image"/>'))
        opf.getroot().append(etree.fromstring('<guide><reference href="cover.html" type="cover" title="Okładka"/></guide>'))


    annotations = etree.Element('annotations')

    toc_file = etree.fromstring('<?xml version="1.0" encoding="utf-8"?><!DOCTYPE ncx PUBLIC ' \
                               '"-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">' \
                               '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" xml:lang="pl" ' \
                               'version="2005-1"><head></head><docTitle></docTitle><navMap>' \
                               '<navPoint id="NavPoint-1" playOrder="1"><navLabel>' \
                               '<text>Strona tytułowa</text></navLabel><content src="title.html" />' \
                               '</navPoint></navMap></ncx>')
    nav_map = toc_file[-1]

    toc, chunk_counter, chars, sample = transform_file(input_xml, sample=sample)

    if not toc.children:
        toc.add(u"Początek utworu", 1)
    toc_counter = toc.write_to_xml(nav_map, 2)

    # Last modifications in container files and EPUB creation
    if len(annotations) > 0:
        nav_map.append(etree.fromstring(
            '<navPoint id="NavPoint-%(i)d" playOrder="%(i)d" ><navLabel><text>Przypisy</text>'\
            '</navLabel><content src="annotations.html" /></navPoint>' % {'i': toc_counter}))
        toc_counter += 1
        manifest.append(etree.fromstring(
            '<item id="annotations" href="annotations.html" media-type="application/xhtml+xml" />'))
        spine.append(etree.fromstring(
            '<itemref idref="annotations" />'))
        replace_by_verse(annotations)
        html_tree = xslt(annotations, get_resource('epub/xsltAnnotations.xsl'))
        chars = chars.union(used_chars(html_tree.getroot()))
        zip.writestr('OPS/annotations.html', etree.tostring(
                            html_tree, method="html", pretty_print=True))

    nav_map.append(etree.fromstring(
        '<navPoint id="NavPoint-%(i)d" playOrder="%(i)d" ><navLabel><text>Strona redakcyjna</text>'\
        '</navLabel><content src="last.html" /></navPoint>' % {'i': toc_counter}))
    manifest.append(etree.fromstring(
        '<item id="last" href="last.html" media-type="application/xhtml+xml" />'))
    spine.append(etree.fromstring(
        '<itemref idref="last" />'))
    html_tree = xslt(input_xml, get_resource('epub/xsltLast.xsl'))
    chars.update(used_chars(html_tree.getroot()))
    zip.writestr('OPS/last.html', etree.tostring(
                        html_tree, method="html", pretty_print=True))

    # strip fonts
    tmpdir = mkdtemp('-librarian-epub')
    cwd = os.getcwd()

    os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font-optimizer'))
    for fname in 'DejaVuSerif.ttf', 'DejaVuSerif-Bold.ttf', 'DejaVuSerif-Italic.ttf', 'DejaVuSerif-BoldItalic.ttf':
        optimizer_call = ['perl', 'subset.pl', '--chars', ''.join(chars).encode('utf-8'),
                          get_resource('fonts/' + fname), os.path.join(tmpdir, fname)]
        if verbose:
            print "Running font-optimizer"
            subprocess.check_call(optimizer_call)
        else:
            subprocess.check_call(optimizer_call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        zip.write(os.path.join(tmpdir, fname), os.path.join('OPS', fname))
    rmtree(tmpdir)
    os.chdir(cwd)

    zip.writestr('OPS/content.opf', etree.tostring(opf, pretty_print=True))
    contents = []
    title = node_name(etree.ETXPath('.//'+DCNS('title'))(input_xml)[0])
    attributes = "dtb:uid", "dtb:depth", "dtb:totalPageCount", "dtb:maxPageNumber"
    for st in attributes:
        meta = toc_file.makeelement(NCXNS('meta'))
        meta.set('name', st)
        meta.set('content', '0')
        toc_file[0].append(meta)
    toc_file[0][0].set('content', ''.join((title, 'WolneLektury.pl')))
    toc_file[0][1].set('content', str(toc.depth()))
    set_inner_xml(toc_file[1], ''.join(('<text>', title, '</text>')))
    zip.writestr('OPS/toc.ncx', etree.tostring(toc_file, pretty_print=True))
    zip.close()
