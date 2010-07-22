# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.  
#
from __future__ import with_statement

import os
import os.path
import shutil
import sys
from copy import deepcopy
from lxml import etree
import zipfile

from librarian import XMLNamespace, RDFNS, DCNS, WLNS, XHTMLNS, NoDublinCore

NCXNS = XMLNamespace("http://www.daisy.org/z3986/2005/ncx/")
OPFNS = XMLNamespace("http://www.idpf.org/2007/opf")


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


_resdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'epub')
def res(fname):
    return os.path.join(_resdir, fname)


def replace_characters(node):
    def replace_chars(text):
        if text is None:
            return None
        return text.replace("&", "&amp;")\
                   .replace("---", "&#8212;")\
                   .replace("--", "&#8211;")\
                   .replace(",,", "&#8222;")\
                   .replace('"', "&#8221;")\
                   .replace("'", "&#8217;")
    if node.tag == 'extra':
        node.clear()
    else:
        node.text = replace_chars(node.text)
        node.tail = replace_chars(node.tail)
        for child in node:
            replace_characters(child)


def find_annotations(annotations, source, part_number):
    for child in source:
        if child.tag in ('pe', 'pa', 'pt', 'pr'):
            annotation = deepcopy(child)
            annotation.set('number', str(len(annotations)+1))
            annotation.set('part', str(part_number))
            annotation.tail = ''
            annotations.append(annotation)
            tail = child.tail
            child.clear()
            child.tail = tail
            child.text = str(len(annotations))
        if child.tag not in ('extra', 'podtytul'):
            find_annotations(annotations, child, part_number)


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


def add_nav_point(nav_map, counter, title, part_counter):
    nav_point = nav_map.makeelement(NCXNS('navPoint'))
    nav_point.set('id', 'NavPoint-%d' % counter)
    nav_point.set('playOrder', str(counter))

    nav_label = nav_map.makeelement(NCXNS('navLabel'))
    text = nav_map.makeelement(NCXNS('text'))
    text.text = title
    nav_label.append(text)
    nav_point.append(nav_label)

    content = nav_map.makeelement(NCXNS('content'))
    content.set('src', 'part%d.html' % part_counter)
    nav_point.append(content)

    nav_map.append(nav_point)


def add_nav_point2(nav_map, counter, title, part_counter, subcounter):
    nav_point = nav_map.makeelement(NCXNS('navPoint'))
    nav_point.set('id', 'NavPoint-%d' % counter)
    nav_point.set('playOrder', str(counter))

    nav_label = nav_map.makeelement(NCXNS('navLabel'))
    text = nav_map.makeelement(NCXNS('text'))
    text.text = title
    nav_label.append(text)
    nav_point.append(nav_label)

    content = nav_map.makeelement(NCXNS('content'))
    content.set('src', 'part%d.html#sub%d' % (part_counter, subcounter))
    nav_point.append(content)

    nav_map[-1].append(nav_point)


def transform(input_file, output_file):
    """ produces an epub

    input_file and output_file should be filelike objects
    """

    input_xml = etree.parse(input_file)

    zip = zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED)

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

    metadata_el = input_xml.find('.//'+RDFNS('Description'))
    if metadata_el is None:
        raise NoDublinCore('Document has no DublinCore - which is required.')
    metadatasource = etree.ElementTree(metadata_el)

    opf = xslt(metadatasource, res('xsltContent.xsl'))

    manifest = opf.find('.//' + OPFNS('manifest'))
    spine = opf.find('.//' + OPFNS('spine'))

    for fname in 'style.css', 'logo_wolnelektury.png':
        zip.write(res(fname), os.path.join('OPS', fname))

    annotations = etree.Element('annotations')
    part_xml = etree.Element('utwor')
    etree.SubElement(part_xml, 'master')

    toc_file = etree.fromstring('<?xml version="1.0" encoding="utf-8"?><!DOCTYPE ncx PUBLIC ' \
                               '"-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">' \
                               '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" xml:lang="pl" ' \
                               'version="2005-1"><head></head><docTitle></docTitle><navMap>' \
                               '<navPoint id="NavPoint-1" playOrder="1"><navLabel>' \
                               '<text>Strona tytułowa</text></navLabel><content src="title.html" />' \
                               '</navPoint><navPoint id="NavPoint-2" playOrder="2"><navLabel>' \
                               '<text>Początek utworu</text></navLabel><content src="part1.html" />' \
                               '</navPoint></navMap></ncx>')

    main_xml_part = part_xml[0] # było [0][0], master
    nav_map = toc_file[-1] # było [-1][-1]
    depth = 1 # navmap

    if len(input_xml.getroot()) > 1:
        # rdf before style master
        main_text = input_xml.getroot()[1]
    else:
        # rdf in style master
        main_text = input_xml.getroot()[0]

    replace_characters(main_text)
    zip.writestr('OPS/title.html', 
                 etree.tostring(xslt(input_xml, res('xsltTitle.xsl')), pretty_print=True))

    # Search for table of contents elements and book division

    stupid_i = stupid_j = stupid_k = 1
    last_node_part = False
    for one_part in main_text:
        name = one_part.tag
        if name in ("naglowek_czesc", "naglowek_rozdzial", "naglowek_akt", "srodtytul"):
            if name == "naglowek_czesc":
                stupid_k = 1
                last_node_part = True
                find_annotations(annotations, part_xml, stupid_j)
                replace_by_verse(part_xml)
                zip.writestr('OPS/part%d.html' % stupid_j,
                            etree.tostring(xslt(part_xml, res('xsltScheme.xsl')), pretty_print=True))
                main_xml_part[:] = [deepcopy(one_part)]
                # add to manifest and spine
                add_to_manifest(manifest, stupid_j)
                add_to_spine(spine, stupid_j)
                name_toc = node_name(one_part)
                # build table of contents
                # i+2 because of title page
                add_nav_point(nav_map, stupid_i+2, name_toc, stupid_j + 1)
                stupid_i += 1
                stupid_j += 1
            else:
                if last_node_part:
                    main_xml_part.append(one_part)
                    last_node_part = False
                    name_toc = node_name(one_part)
                    add_nav_point(nav_map, stupid_i + 1, name_toc, stupid_j)
                else:
                    stupid_k = 1
                    find_annotations(annotations, part_xml, stupid_j)
                    replace_by_verse(part_xml)
                    zip.writestr('OPS/part%d.html' % stupid_j,
                                 etree.tostring(xslt(part_xml, res('xsltScheme.xsl')), pretty_print=True))
                    # start building a new part
                    main_xml_part[:] = [deepcopy(one_part)]
                    add_to_manifest(manifest, stupid_j)
                    add_to_spine(spine, stupid_j)
                    name_toc = node_name(one_part)
                    add_nav_point(nav_map, stupid_i + 2, name_toc, stupid_j + 1) # title page
                    stupid_j += 1
                    stupid_i += 1
        else:
            if name in ('naglowek_podrozdzial', 'naglowek_scena'):
                depth = 2
                name_toc =  node_name(one_part)
                add_nav_point2(nav_map, stupid_i + 2, name_toc, stupid_j, stupid_k)
                one_part.set('sub', str(stupid_k))
                stupid_k += 1
                stupid_i += 1
            main_xml_part.append(deepcopy(one_part))
            last_node_part = False
    find_annotations(annotations, part_xml, stupid_j)
    replace_by_verse(part_xml)
    add_to_manifest(manifest, stupid_j)
    add_to_spine(spine, stupid_j)

    zip.writestr('OPS/part%d.html' % stupid_j,
                 etree.tostring(xslt(part_xml, res('xsltScheme.xsl')), pretty_print=True))

    # Last modifications in container files and EPUB creation
    if len(annotations) > 0:
        nav_map.append(etree.fromstring(
            '<navPoint id="NavPoint-%(i)d" playOrder="%(i)d" ><navLabel><text>Przypisy</text>'\
            '</navLabel><content src="annotations.html" /></navPoint>' % {'i':stupid_i+2}))
        manifest.append(etree.fromstring(
            '<item id="annotations" href="annotations.html" media-type="application/xhtml+xml" />'))
        spine.append(etree.fromstring(
            '<itemref idref="annotations" />'))
        replace_by_verse(annotations)
        zip.writestr('OPS/annotations.html', etree.tostring(
                            xslt(annotations, res("xsltAnnotations.xsl")), pretty_print=True))

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
    toc_file[0][1].set('content', str(depth))
    set_inner_xml(toc_file[1], ''.join(('<text>', title, '</text>')))
    zip.writestr('OPS/toc.ncx', etree.tostring(toc_file, pretty_print=True))
    zip.close()


if __name__ == '__main__':
    import html

    if len(sys.argv) < 2:
        print >> sys.stderr, 'Usage: python epub.py <input file> [output file]'
        sys.exit(1)

    input = sys.argv[1]
    if len(sys.argv) > 2:
        output = sys.argv[2]
    else:
        basename, ext = os.path.splitext(input)
        output = basename + '.epub' 

    print input
    if html.transform(input, is_file=True) == '<empty />':
        print 'empty content - skipping'
    else:
        transform(open(input, 'r'), open(output, 'w'))



