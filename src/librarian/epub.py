# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from __future__ import print_function, unicode_literals

import os
import os.path
import re
import subprocess
import six
from copy import deepcopy
from mimetypes import guess_type

from ebooklib import epub
from lxml import etree
from tempfile import mkdtemp, NamedTemporaryFile
from shutil import rmtree

from librarian import RDFNS, WLNS, DCNS, OutputFile
from librarian.cover import make_cover

from librarian import functions, get_resource

from librarian.hyphenator import Hyphenator

functions.reg_person_name()


def squeeze_whitespace(s):
    return re.sub(b'\\s+', b' ', s)


def set_hyph_language(source_tree):
    bibl_lng = etree.XPath('//dc:language//text()',
                           namespaces={'dc': str(DCNS)})(source_tree)
    short_lng = functions.lang_code_3to2(bibl_lng[0])
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

    >>> print(inner_xml(etree.fromstring('<a>x<b>y</b>z</a>')))
    x<b>y</b>z
    """

    nt = node.text if node.text is not None else ''
    return ''.join(
        [nt] + [etree.tostring(child, encoding='unicode') for child in node]
    )


def set_inner_xml(node, text):
    """ sets node's text and children from a string

    >>> e = etree.fromstring('<a>b<b>x</b>x</a>')
    >>> set_inner_xml(e, 'x<b>y</b>z')
    >>> print(etree.tostring(e, encoding='unicode'))
    <a>x<b>y</b>z</a>
    """

    p = etree.fromstring('<x>%s</x>' % text)
    node.text = p.text
    node[:] = p[:]


def node_name(node):
    """ Find out a node's name

    >>> print(node_name(etree.fromstring('<a>X<b>Y</b>Z</a>')))
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


def xslt(xml, sheet, **kwargs):
    if isinstance(xml, etree._Element):
        xml = etree.ElementTree(xml)
    with open(sheet) as xsltf:
        transform = etree.XSLT(etree.parse(xsltf))
        params = dict(
            (key, transform.strparam(value))
            for key, value in kwargs.items()
        )
        return transform(xml, **params)


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

    >>> s = etree.fromstring(
    ...         "<strofa>a <b>c</b> <b>c</b>/\\nb<x>x/\\ny</x>c/ \\nd</strofa>"
    ...     )
    >>> Stanza(s).versify()
    >>> print(etree.tostring(s, encoding='unicode', pretty_print=True).strip())
    <strofa>
      <wers_normalny>a <b>c</b><b>c</b></wers_normalny>
      <wers_normalny>b<x>x/
    y</x>c</wers_normalny>
      <wers_normalny>d</wers_normalny>
    </strofa>

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
        self.stanza.extend(
            verse for verse in self.verses
            if verse.text or len(verse) > 0
        )

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
            if not verse_text.strip():
                continue
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

    # The below loop are workaround for a problem with epubs
    # in drama ebooks without acts.
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
            elif (not last_node_part
                  and name in (
                      "naglowek_rozdzial", "naglowek_akt", "srodtytul"
                  )):
                yield part_xml
                main_xml_part[:] = [deepcopy(one_part)]
            else:
                main_xml_part.append(deepcopy(one_part))
                last_node_part = False
    yield part_xml


def transform_chunk(chunk_xml, chunk_no, annotations, empty=False,
                    _empty_html_static=[]):
    """
    Transforms one chunk, returns a HTML string, a TOC object
    and a set of used characters.
    """

    toc = []
    for element in chunk_xml[0]:
        if element.tag == "naglowek_czesc":
            toc.append(
                (
                    epub.Link(
                        "part%d.xhtml#book-text" % chunk_no,
                        node_name(element),
                        "part%d-text" % chunk_no
                    ),
                    []
                )
            )
        elif element.tag in ("naglowek_rozdzial", "naglowek_akt", "srodtytul"):
            toc.append(
                (
                    epub.Link(
                        "part%d.xhtml" % chunk_no,
                        node_name(element),
                        "part%d" % chunk_no
                    ),
                    []
                )
            )
        elif element.tag in ('naglowek_podrozdzial', 'naglowek_scena'):
            subnumber = len(toc[-1][1])
            toc[-1][1].append(
                epub.Link(
                    "part%d.xhtml#sub%d" % (chunk_no, subnumber),
                    node_name(element),
                    "part%d-sub%d" % (chunk_no, subnumber)
                )
            )
            element.set('sub', six.text_type(subnumber))
    if empty:
        if not _empty_html_static:
            with open(get_resource('epub/emptyChunk.xhtml')) as f:
                _empty_html_static.append(f.read())
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
            doctype='<!DOCTYPE html>'
        )
    return output_html, toc, chars


def remove_empty_lists_from_toc(toc):
    for i, e in enumerate(toc):
        if isinstance(e, tuple):
            if e[1]:
                remove_empty_lists_from_toc(e[1])
            else:
                toc[i] = e[0]


def transform(wldoc, verbose=False, style=None,
              sample=None, cover=None, flags=None, hyphenate=False,
              ilustr_path='', output_type='epub'):
    """ produces a EPUB file

    sample=n: generate sample e-book (with at least n paragraphs)
    cover: a cover.Cover factory or True for default
    flags: less-advertising, without-fonts, working-copy
    """

    def transform_file(wldoc, chunk_counter=1, first=True, sample=None):
        """ processes one input file and proceeds to its children """

        replace_characters(wldoc.edoc.getroot())

        hyphenator = set_hyph_language(
            wldoc.edoc.getroot()
        ) if hyphenate else None
        hyphenate_and_fix_conjunctions(wldoc.edoc.getroot(), hyphenator)

        # every input file will have a TOC entry,
        # pointing to starting chunk
        toc = [
            (
                epub.Link(
                    "part%d.xhtml" % chunk_counter,
                    wldoc.book_info.title,
                    "path%d-start" % chunk_counter
                ),
                []
            )
        ]
        chars = set()
        if first:
            # write book title page
            html_tree = xslt(wldoc.edoc, get_resource('epub/xsltTitle.xsl'),
                             outputtype=output_type)
            chars = used_chars(html_tree.getroot())
            html_string = etree.tostring(
                html_tree, pretty_print=True, xml_declaration=True,
                encoding="utf-8",
                doctype='<!DOCTYPE html>'
            )
            item = epub.EpubItem(
                uid="titlePage",
                file_name="title.xhtml",
                media_type="application/xhtml+xml",
                content=squeeze_whitespace(html_string)
            )
            spine.append(item)
            output.add_item(item)
            # add a title page TOC entry
            toc[-1][1].append(
                epub.Link(
                    "title.xhtml",
                    "Strona tytułowa",
                    "title",
                )
            )

            item = epub.EpubNav()
            toc[-1][1].append(
                epub.Link(
                    "nav.xhtml",
                    "Spis treści",
                    "nav"
                )
            )
            output.add_item(item)
            spine.append(item)

        elif wldoc.book_info.parts:
            # write title page for every parent
            if sample is not None and sample <= 0:
                chars = set()
                html_string = open(
                    get_resource('epub/emptyChunk.xhtml')).read()
            else:
                html_tree = xslt(wldoc.edoc,
                                 get_resource('epub/xsltChunkTitle.xsl'))
                chars = used_chars(html_tree.getroot())
                html_string = etree.tostring(
                    html_tree, pretty_print=True, xml_declaration=True,
                    encoding="utf-8",
                    doctype='<!DOCTYPE html>'
                )
            item = epub.EpubItem(
                uid="part%d" % chunk_counter,
                file_name="part%d.xhtml" % chunk_counter,
                media_type="application/xhtml+xml",
                content=squeeze_whitespace(html_string)
            )
            output.add_item(item)
            spine.append(item)

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
                        sample -= len(chunk_xml.xpath(
                            '//strofa|//akap|//akap_cd|//akap_dialog'
                        ))
                chunk_html, chunk_toc, chunk_chars = transform_chunk(
                    chunk_xml, chunk_counter, annotations, empty)

                toc[-1][1].extend(chunk_toc)
                chars = chars.union(chunk_chars)
                item = epub.EpubItem(
                    uid="part%d" % chunk_counter,
                    file_name="part%d.xhtml" % chunk_counter,
                    media_type="application/xhtml+xml",
                    content=squeeze_whitespace(chunk_html)
                )
                output.add_item(item)
                spine.append(item)
                chunk_counter += 1

        for child in wldoc.parts():
            child_toc, chunk_counter, chunk_chars, sample = transform_file(
                child, chunk_counter, first=False, sample=sample)
            toc[-1][1].extend(child_toc)
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

    output = epub.EpubBook()
    output.set_identifier(six.text_type(document.book_info.url))
    output.set_language(functions.lang_code_3to2(document.book_info.language))
    output.set_title(document.book_info.title)
    for author in document.book_info.authors:
        output.add_author(
            author.readable(),
            file_as=six.text_type(author)
        )
    for translator in document.book_info.translators:
        output.add_author(
            translator.readable(),
            file_as=six.text_type(translator),
            role='translator'
        )
    for publisher in document.book_info.publisher:
        output.add_metadata("DC", "publisher", publisher)
    output.add_metadata("DC", "date", document.book_info.created_at)

    output.guide.append({
        "type": "text",
        "title": "Początek",
        "href": "part1.xhtml"
    })

    output.add_item(epub.EpubNcx())

    spine = output.spine

    functions.reg_mathml_epub(output)

    if os.path.isdir(ilustr_path):
        ilustr_elements = set(ilustr.get('src')
                              for ilustr in document.edoc.findall('//ilustr'))
        for i, filename in enumerate(os.listdir(ilustr_path)):
            if filename not in ilustr_elements:
                continue
            file_path = os.path.join(ilustr_path, filename)
            with open(file_path, 'rb') as f:
                output.add_item(
                    epub.EpubItem(
                        uid='image%s' % i,
                        file_name=filename,
                        media_type=guess_type(file_path)[0],
                        content=f.read()
                    )
                )

    # write static elements

    with open(get_resource('res/wl-logo-small.png'), 'rb') as f:
        output.add_item(
            epub.EpubItem(
                uid="logo_wolnelektury.png",
                file_name="logo_wolnelektury.png",
                media_type="image/png",
                content=f.read()
            )
        )
    with open(get_resource('res/jedenprocent.png'), 'rb') as f:
        output.add_item(
            epub.EpubItem(
                uid="jedenprocent",
                file_name="jedenprocent.png",
                media_type="image/png",
                content=f.read()
            )
        )

    if not style:
        style = get_resource('epub/style.css')
    with open(style, 'rb') as f:
        output.add_item(
            epub.EpubItem(
                uid="style",
                file_name="style.css",
                media_type="text/css",
                content=f.read()
            )
        )

    if cover:
        if cover is True:
            cover = make_cover

        cover_file = six.BytesIO()
        bound_cover = cover(document.book_info)
        bound_cover.save(cover_file)
        cover_name = 'cover.%s' % bound_cover.ext()

        output.set_cover(
            file_name=cover_name,
            content=cover_file.getvalue(),
        )
        spine.append('cover')
        output.guide.append({
            "type": "cover",
            "href": "cover.xhtml",
            "title": "Okładka",
        })

        del cover_file

        if bound_cover.uses_dc_cover:
            if document.book_info.cover_by:
                document.edoc.getroot().set('data-cover-by',
                                            document.book_info.cover_by)
            if document.book_info.cover_source:
                document.edoc.getroot().set('data-cover-source',
                                            document.book_info.cover_source)

    annotations = etree.Element('annotations')

    toc, chunk_counter, chars, sample = transform_file(document, sample=sample)
    output.toc = toc[0][1]

    if len(toc) < 2:
        toc.append(
            epub.Link(
                "part1.xhtml",
                "Początek utworu",
                "part1"
            )
        )

    # Last modifications in container files and EPUB creation
    if len(annotations) > 0:
        toc.append(
            epub.Link(
                "annotations.xhtml",
                "Przypisy",
                "annotations"
            )
        )
        replace_by_verse(annotations)
        html_tree = xslt(annotations, get_resource('epub/xsltAnnotations.xsl'))
        chars = chars.union(used_chars(html_tree.getroot()))

        item = epub.EpubItem(
            uid="annotations",
            file_name="annotations.xhtml",
            media_type="application/xhtml+xml",
            content=etree.tostring(
                html_tree, pretty_print=True, xml_declaration=True,
                encoding="utf-8",
                doctype='<!DOCTYPE html>'
            )
        )
        output.add_item(item)
        spine.append(item)

    toc.append(
        epub.Link(
            "support.xhtml",
            "Wesprzyj Wolne Lektury",
            "support"
        )
    )
    with open(get_resource('epub/support.xhtml'), 'rb') as f:
        html_string = f.read()
    chars.update(used_chars(etree.fromstring(html_string)))
    item = epub.EpubItem(
        uid="support",
        file_name="support.xhtml",
        media_type="application/xhtml+xml",
        content=squeeze_whitespace(html_string)
    )
    output.add_item(item)
    spine.append(item)

    toc.append(
        epub.Link(
            "last.xhtml",
            "Strona redakcyjna",
            "last"
        )
    )
    html_tree = xslt(document.edoc, get_resource('epub/xsltLast.xsl'),
                     outputtype=output_type)
    chars.update(used_chars(html_tree.getroot()))
    item = epub.EpubItem(
        uid="last",
        file_name="last.xhtml",
        media_type="application/xhtml+xml",
        content=squeeze_whitespace(etree.tostring(
            html_tree, pretty_print=True, xml_declaration=True,
            encoding="utf-8",
            doctype='<!DOCTYPE html>'
        ))
    )
    output.add_item(item)
    spine.append(item)

    if not flags or 'without-fonts' not in flags:
        # strip fonts
        tmpdir = mkdtemp('-librarian-epub')
        try:
            cwd = os.getcwd()
        except OSError:
            cwd = None

        os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              'font-optimizer'))
        for fname in ('DejaVuSerif.ttf', 'DejaVuSerif-Bold.ttf',
                      'DejaVuSerif-Italic.ttf', 'DejaVuSerif-BoldItalic.ttf'):
            optimizer_call = ['perl', 'subset.pl', '--chars',
                              ''.join(chars).encode('utf-8'),
                              get_resource('fonts/' + fname),
                              os.path.join(tmpdir, fname)]
            env = {"PERL_USE_UNSAFE_INC": "1"}
            if verbose:
                print("Running font-optimizer")
                subprocess.check_call(optimizer_call, env=env)
            else:
                dev_null = open(os.devnull, 'w')
                subprocess.check_call(optimizer_call, stdout=dev_null,
                                      stderr=dev_null, env=env)
            with open(os.path.join(tmpdir, fname), 'rb') as f:
                output.add_item(
                    epub.EpubItem(
                        uid=fname,
                        file_name=fname,
                        media_type="font/ttf",
                        content=f.read()
                    )
                )
        rmtree(tmpdir)
        if cwd is not None:
            os.chdir(cwd)

    remove_empty_lists_from_toc(output.toc)

    output_file = NamedTemporaryFile(prefix='librarian', suffix='.epub',
                                     delete=False)
    output_file.close()
    epub.write_epub(output_file.name, output, {'epub3_landmark': False})
    return OutputFile.from_filename(output_file.name)
