# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from __future__ import with_statement

import os
import os.path
import re
import subprocess
from StringIO import StringIO
from copy import deepcopy
from mimetypes import guess_type

from lxml import etree
import zipfile
from tempfile import mkdtemp, NamedTemporaryFile
from shutil import rmtree

from librarian import RDFNS, WLNS, NCXNS, OPFNS, XHTMLNS, DCNS, OutputFile
from librarian.cover import DefaultEbookCover

from librarian import functions, get_resource

from librarian.hyphenator import Hyphenator

functions.reg_person_name()
functions.reg_lang_code_3to2()


def set_hyph_language(source_tree):
    def get_short_lng_code(text):
        result = ''
        text = ''.join(text)
        with open(get_resource('res/ISO-639-2_8859-1.txt'), 'rb') as f:
            for line in f:
                list = line.strip().split('|')
                if list[0] == text:
                    result = list[2]
        if result == '':
            return text
        else:
            return result
    bibl_lng = etree.XPath('//dc:language//text()',
                           namespaces={'dc': str(DCNS)})(source_tree)
    short_lng = get_short_lng_code(bibl_lng[0])
    try:
        return Hyphenator(get_resource('res/hyph-dictionaries/hyph_' +
                                       short_lng + '.dic'))
    except:
        pass


def hyphenate_and_fix_conjunctions(source_tree, hyph):
    texts = etree.XPath('/utwor/*[2]//text()')(source_tree)
    for t in texts:
        parent = t.getparent()
        if hyph is not None:
            newt = ''
            wlist = re.compile(r'\w+|[^\w]', re.UNICODE).findall(t)
            for w in wlist:
                newt += hyph.inserted(w, u'\u00AD')
        else:
            newt = t
        newt = re.sub(r'(?<=\s\w)\s+', u'\u00A0', newt)
        if t.is_text:
            parent.text = newt
        elif t.is_tail:
            parent.tail = newt


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
            number = str(len(annotations) + 1)
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


class Stanza(object):
    """
    Converts / verse endings into verse elements in a stanza.

    Slashes may only occur directly in the stanza. Any slashes in subelements
    will be ignored, and the subelements will be put inside verse elements.

    >>> s = etree.fromstring("<strofa>a <b>c</b> <b>c</b>/\\nb<x>x/\\ny</x>c/ \\nd</strofa>")
    >>> Stanza(s).versify()
    >>> print etree.tostring(s)
    <strofa><wers_normalny>a <b>c</b> <b>c</b></wers_normalny><wers_normalny>b<x>x/
    y</x>c</wers_normalny><wers_normalny>d</wers_normalny></strofa>

    """
    def __init__(self, stanza_elem):
        self.stanza = stanza_elem
        self.verses = []
        self.open_verse = None

    def versify(self):
        self.push_text(self.stanza.text)
        for elem in self.stanza:
            self.push_elem(elem)
            self.push_text(elem.tail)
        tail = self.stanza.tail
        self.stanza.clear()
        self.stanza.tail = tail
        self.stanza.extend(self.verses)

    def open_normal_verse(self):
        self.open_verse = self.stanza.makeelement("wers_normalny")
        self.verses.append(self.open_verse)

    def get_open_verse(self):
        if self.open_verse is None:
            self.open_normal_verse()
        return self.open_verse

    def push_text(self, text):
        if not text:
            return
        for i, verse_text in enumerate(re.split(r"/\s*\n", text)):
            if i:
                self.open_normal_verse()
            verse = self.get_open_verse()
            if len(verse):
                verse[-1].tail = (verse[-1].tail or "") + verse_text
            else:
                verse.text = (verse.text or "") + verse_text

    def push_elem(self, elem):
        if elem.tag.startswith("wers"):
            verse = deepcopy(elem)
            verse.tail = None
            self.verses.append(verse)
            self.open_verse = verse
        else:
            appended = deepcopy(elem)
            appended.tail = None
            self.get_open_verse().append(appended)


def replace_by_verse(tree):
    """ Find stanzas and create new verses in place of a '/' character """

    stanzas = tree.findall('.//' + WLNS('strofa'))
    for stanza in stanzas:
        Stanza(stanza).versify()


def add_to_manifest(manifest, partno):
    """ Adds a node to the manifest section in content.opf file """

    partstr = 'part%d' % partno
    e = manifest.makeelement(
        OPFNS('item'), attrib={'id': partstr, 'href': partstr + '.html',
                               'media-type': 'application/xhtml+xml'}
    )
    manifest.append(e)


def add_to_spine(spine, partno):
    """ Adds a node to the spine section in content.opf file """

    e = spine.makeelement(OPFNS('itemref'), attrib={'idref': 'part%d' % partno})
    spine.append(e)


class TOC(object):
    def __init__(self, name=None, part_href=None):
        self.children = []
        self.name = name
        self.part_href = part_href
        self.sub_number = None

    def add(self, name, part_href, level=0, is_part=True, index=None):
        assert level == 0 or index is None
        if level > 0 and self.children:
            return self.children[-1].add(name, part_href, level - 1, is_part)
        else:
            t = TOC(name)
            t.part_href = part_href
            if index is not None:
                self.children.insert(index, t)
            else:
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

    def href(self):
        src = self.part_href
        if self.sub_number is not None:
            src += '#sub%d' % self.sub_number
        return src

    def write_to_xml(self, nav_map, counter=1):
        for child in self.children:
            nav_point = nav_map.makeelement(NCXNS('navPoint'))
            nav_point.set('id', 'NavPoint-%d' % counter)
            nav_point.set('playOrder', str(counter))

            nav_label = nav_map.makeelement(NCXNS('navLabel'))
            text = nav_map.makeelement(NCXNS('text'))
            if child.name is not None:
                text.text = re.sub(r'\n', ' ', child.name)
            else:
                text.text = child.name
            nav_label.append(text)
            nav_point.append(nav_label)

            content = nav_map.makeelement(NCXNS('content'))
            content.set('src', child.href())
            nav_point.append(content)
            nav_map.append(nav_point)
            counter = child.write_to_xml(nav_point, counter + 1)
        return counter

    def html_part(self, depth=0):
        texts = []
        for child in self.children:
            texts.append(
                "<div style='margin-left:%dem;'><a href='%s'>%s</a></div>" %
                (depth, child.href(), child.name))
            texts.append(child.html_part(depth + 1))
        return "\n".join(texts)

    def html(self):
        with open(get_resource('epub/toc.html')) as f:
            t = unicode(f.read(), 'utf-8')
        return t % self.html_part()


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
    main_xml_part = part_xml[0]  # master

    last_node_part = False

    # the below loop are workaround for a problem with epubs in drama ebooks without acts
    is_scene = False
    is_act = False
    for one_part in main_text:
        name = one_part.tag
        if name == 'naglowek_scena':
            is_scene = True
        elif name == 'naglowek_akt':
            is_act = True

    for one_part in main_text:
        name = one_part.tag
        if is_act is False and is_scene is True:
            if name == 'naglowek_czesc':
                yield part_xml
                last_node_part = True
                main_xml_part[:] = [deepcopy(one_part)]
            elif not last_node_part and name == "naglowek_scena":
                yield part_xml
                main_xml_part[:] = [deepcopy(one_part)]
            else:
                main_xml_part.append(deepcopy(one_part))
                last_node_part = False
        else:
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
        if element.tag == "naglowek_czesc":
            toc.add(node_name(element), "part%d.html#book-text" % chunk_no)
        elif element.tag in ("naglowek_rozdzial", "naglowek_akt", "srodtytul"):
            toc.add(node_name(element), "part%d.html" % chunk_no)
        elif element.tag in ('naglowek_podrozdzial', 'naglowek_scena'):
            subnumber = toc.add(node_name(element), "part%d.html" % chunk_no, level=1, is_part=False)
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
        output_html = etree.tostring(
            html_tree, pretty_print=True, xml_declaration=True,
            encoding="utf-8",
            doctype='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" ' +
                    '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'
        )
    return output_html, toc, chars


def transform(wldoc, verbose=False, style=None, html_toc=False,
              sample=None, cover=None, flags=None, hyphenate=False, ilustr_path=''):
    """ produces a EPUB file

    sample=n: generate sample e-book (with at least n paragraphs)
    cover: a cover.Cover factory or True for default
    flags: less-advertising, without-fonts, working-copy
    """

    def transform_file(wldoc, chunk_counter=1, first=True, sample=None):
        """ processes one input file and proceeds to its children """

        replace_characters(wldoc.edoc.getroot())

        hyphenator = set_hyph_language(wldoc.edoc.getroot()) if hyphenate else None
        hyphenate_and_fix_conjunctions(wldoc.edoc.getroot(), hyphenator)

        # every input file will have a TOC entry,
        # pointing to starting chunk
        toc = TOC(wldoc.book_info.title, "part%d.html" % chunk_counter)
        chars = set()
        if first:
            # write book title page
            html_tree = xslt(wldoc.edoc, get_resource('epub/xsltTitle.xsl'))
            chars = used_chars(html_tree.getroot())
            zip.writestr(
                'OPS/title.html',
                etree.tostring(
                    html_tree, pretty_print=True, xml_declaration=True,
                    encoding="utf-8",
                    doctype='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"' +
                            ' "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'
                )
            )
            # add a title page TOC entry
            toc.add(u"Strona tytułowa", "title.html")
        elif wldoc.book_info.parts:
            # write title page for every parent
            if sample is not None and sample <= 0:
                chars = set()
                html_string = open(get_resource('epub/emptyChunk.html')).read()
            else:
                html_tree = xslt(wldoc.edoc, get_resource('epub/xsltChunkTitle.xsl'))
                chars = used_chars(html_tree.getroot())
                html_string = etree.tostring(
                    html_tree, pretty_print=True, xml_declaration=True,
                    encoding="utf-8",
                    doctype='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"' +
                            ' "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'
                )
            zip.writestr('OPS/part%d.html' % chunk_counter, html_string)
            add_to_manifest(manifest, chunk_counter)
            add_to_spine(spine, chunk_counter)
            chunk_counter += 1

        if len(wldoc.edoc.getroot()) > 1:
            # rdf before style master
            main_text = wldoc.edoc.getroot()[1]
        else:
            # rdf in style master
            main_text = wldoc.edoc.getroot()[0]
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

        for child in wldoc.parts():
            child_toc, chunk_counter, chunk_chars, sample = transform_file(
                child, chunk_counter, first=False, sample=sample)
            toc.append(child_toc)
            chars = chars.union(chunk_chars)

        return toc, chunk_counter, chars, sample

    document = deepcopy(wldoc)
    del wldoc

    if flags:
        for flag in flags:
            document.edoc.getroot().set(flag, 'yes')

    document.clean_ed_note()
    document.clean_ed_note('abstrakt')

    # add editors info
    editors = document.editors()
    if editors:
        document.edoc.getroot().set('editors', u', '.join(sorted(
            editor.readable() for editor in editors)))
    if document.book_info.funders:
        document.edoc.getroot().set('funders', u', '.join(
            document.book_info.funders))
    if document.book_info.thanks:
        document.edoc.getroot().set('thanks', document.book_info.thanks)

    opf = xslt(document.book_info.to_etree(), get_resource('epub/xsltContent.xsl'))
    manifest = opf.find('.//' + OPFNS('manifest'))
    guide = opf.find('.//' + OPFNS('guide'))
    spine = opf.find('.//' + OPFNS('spine'))

    output_file = NamedTemporaryFile(prefix='librarian', suffix='.epub', delete=False)
    zip = zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED)

    functions.reg_mathml_epub(zip)

    if os.path.isdir(ilustr_path):
        for i, filename in enumerate(os.listdir(ilustr_path)):
            file_path = os.path.join(ilustr_path, filename)
            zip.write(file_path, os.path.join('OPS', filename))
            image_id = 'image%s' % i
            manifest.append(etree.fromstring(
                '<item id="%s" href="%s" media-type="%s" />' % (image_id, filename, guess_type(file_path)[0])))

    # write static elements
    mime = zipfile.ZipInfo()
    mime.filename = 'mimetype'
    mime.compress_type = zipfile.ZIP_STORED
    mime.extra = ''
    zip.writestr(mime, 'application/epub+zip')
    zip.writestr(
        'META-INF/container.xml',
        '<?xml version="1.0" ?>'
        '<container version="1.0" '
        'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
        '<rootfiles><rootfile full-path="OPS/content.opf" '
        'media-type="application/oebps-package+xml" />'
        '</rootfiles></container>'
    )
    zip.write(get_resource('res/wl-logo-small.png'),
              os.path.join('OPS', 'logo_wolnelektury.png'))
    zip.write(get_resource('res/jedenprocent.png'),
              os.path.join('OPS', 'jedenprocent.png'))
    if not style:
        style = get_resource('epub/style.css')
    zip.write(style, os.path.join('OPS', 'style.css'))

    if cover:
        if cover is True:
            cover = DefaultEbookCover

        cover_file = StringIO()
        bound_cover = cover(document.book_info)
        bound_cover.save(cover_file)
        cover_name = 'cover.%s' % bound_cover.ext()
        zip.writestr(os.path.join('OPS', cover_name), cover_file.getvalue())
        del cover_file

        cover_tree = etree.parse(get_resource('epub/cover.html'))
        cover_tree.find('//' + XHTMLNS('img')).set('src', cover_name)
        zip.writestr('OPS/cover.html', etree.tostring(
            cover_tree, pretty_print=True, xml_declaration=True,
            encoding="utf-8",
            doctype='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" ' +
                    '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'
        ))

        if bound_cover.uses_dc_cover:
            if document.book_info.cover_by:
                document.edoc.getroot().set('data-cover-by', document.book_info.cover_by)
            if document.book_info.cover_source:
                document.edoc.getroot().set('data-cover-source', document.book_info.cover_source)

        manifest.append(etree.fromstring(
            '<item id="cover" href="cover.html" media-type="application/xhtml+xml" />'))
        manifest.append(etree.fromstring(
            '<item id="cover-image" href="%s" media-type="%s" />' % (cover_name, bound_cover.mime_type())))
        spine.insert(0, etree.fromstring('<itemref idref="cover"/>'))
        opf.getroot()[0].append(etree.fromstring('<meta name="cover" content="cover-image"/>'))
        guide.append(etree.fromstring('<reference href="cover.html" type="cover" title="Okładka"/>'))

    annotations = etree.Element('annotations')

    toc_file = etree.fromstring(
        '<?xml version="1.0" encoding="utf-8"?><!DOCTYPE ncx PUBLIC '
        '"-//NISO//DTD ncx 2005-1//EN" '
        '"http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">'
        '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" xml:lang="pl" '
        'version="2005-1"><head></head><docTitle></docTitle><navMap>'
        '</navMap></ncx>'
    )
    nav_map = toc_file[-1]

    if html_toc:
        manifest.append(etree.fromstring(
            '<item id="html_toc" href="toc.html" media-type="application/xhtml+xml" />'))
        spine.append(etree.fromstring(
            '<itemref idref="html_toc" />'))
        guide.append(etree.fromstring('<reference href="toc.html" type="toc" title="Spis treści"/>'))

    toc, chunk_counter, chars, sample = transform_file(document, sample=sample)

    if len(toc.children) < 2:
        toc.add(u"Początek utworu", "part1.html")

    # Last modifications in container files and EPUB creation
    if len(annotations) > 0:
        toc.add("Przypisy", "annotations.html")
        manifest.append(etree.fromstring(
            '<item id="annotations" href="annotations.html" media-type="application/xhtml+xml" />'))
        spine.append(etree.fromstring(
            '<itemref idref="annotations" />'))
        replace_by_verse(annotations)
        html_tree = xslt(annotations, get_resource('epub/xsltAnnotations.xsl'))
        chars = chars.union(used_chars(html_tree.getroot()))
        zip.writestr('OPS/annotations.html', etree.tostring(
            html_tree, pretty_print=True, xml_declaration=True,
            encoding="utf-8",
            doctype='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" ' +
                    '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'
        ))

    toc.add("Wesprzyj Wolne Lektury", "support.html")
    manifest.append(etree.fromstring(
        '<item id="support" href="support.html" media-type="application/xhtml+xml" />'))
    spine.append(etree.fromstring(
        '<itemref idref="support" />'))
    html_string = open(get_resource('epub/support.html')).read()
    chars.update(used_chars(etree.fromstring(html_string)))
    zip.writestr('OPS/support.html', html_string)

    toc.add("Strona redakcyjna", "last.html")
    manifest.append(etree.fromstring(
        '<item id="last" href="last.html" media-type="application/xhtml+xml" />'))
    spine.append(etree.fromstring(
        '<itemref idref="last" />'))
    html_tree = xslt(document.edoc, get_resource('epub/xsltLast.xsl'))
    chars.update(used_chars(html_tree.getroot()))
    zip.writestr('OPS/last.html', etree.tostring(
        html_tree, pretty_print=True, xml_declaration=True,
        encoding="utf-8",
        doctype='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" ' +
                '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'
    ))

    if not flags or 'without-fonts' not in flags:
        # strip fonts
        tmpdir = mkdtemp('-librarian-epub')
        try:
            cwd = os.getcwd()
        except OSError:
            cwd = None

        os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font-optimizer'))
        for fname in 'DejaVuSerif.ttf', 'DejaVuSerif-Bold.ttf', 'DejaVuSerif-Italic.ttf', 'DejaVuSerif-BoldItalic.ttf':
            optimizer_call = ['perl', 'subset.pl', '--chars',
                              ''.join(chars).encode('utf-8'),
                              get_resource('fonts/' + fname),
                              os.path.join(tmpdir, fname)]
            if verbose:
                print "Running font-optimizer"
                subprocess.check_call(optimizer_call)
            else:
                subprocess.check_call(optimizer_call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            zip.write(os.path.join(tmpdir, fname), os.path.join('OPS', fname))
            manifest.append(etree.fromstring(
                '<item id="%s" href="%s" media-type="application/x-font-truetype" />' % (fname, fname)))
        rmtree(tmpdir)
        if cwd is not None:
            os.chdir(cwd)
    zip.writestr('OPS/content.opf', etree.tostring(opf, pretty_print=True,
                 xml_declaration=True, encoding="utf-8"))
    title = document.book_info.title
    attributes = "dtb:uid", "dtb:depth", "dtb:totalPageCount", "dtb:maxPageNumber"
    for st in attributes:
        meta = toc_file.makeelement(NCXNS('meta'))
        meta.set('name', st)
        meta.set('content', '0')
        toc_file[0].append(meta)
    toc_file[0][0].set('content', str(document.book_info.url))
    toc_file[0][1].set('content', str(toc.depth()))
    set_inner_xml(toc_file[1], ''.join(('<text>', title, '</text>')))

    # write TOC
    if html_toc:
        toc.add(u"Spis treści", "toc.html", index=1)
        zip.writestr('OPS/toc.html', toc.html().encode('utf-8'))
    toc.write_to_xml(nav_map)
    zip.writestr('OPS/toc.ncx', etree.tostring(toc_file, pretty_print=True,
                 xml_declaration=True, encoding="utf-8"))
    zip.close()

    return OutputFile.from_filename(output_file.name)
