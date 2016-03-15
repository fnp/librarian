# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import os
import re
import cStringIO
import copy

from lxml import etree
from librarian import XHTMLNS, ParseError, OutputFile
from librarian import functions

from lxml.etree import XMLSyntaxError, XSLTApplyError

functions.reg_substitute_entities()
functions.reg_person_name()

STYLESHEETS = {
    'legacy': 'xslt/book2html.xslt',
    'full': 'xslt/wl2html_full.xslt',
    'partial': 'xslt/wl2html_partial.xslt'
}


def get_stylesheet(name):
    return os.path.join(os.path.dirname(__file__), STYLESHEETS[name])


def html_has_content(text):
    return etree.ETXPath('//p|//{%(ns)s}p|//h1|//{%(ns)s}h1' % {'ns': str(XHTMLNS)})(text)


def transform(wldoc, stylesheet='legacy', options=None, flags=None):
    """Transforms the WL document to XHTML.

    If output_filename is None, returns an XML,
    otherwise returns True if file has been written,False if it hasn't.
    File won't be written if it has no content.
    """
    # Parse XSLT
    try:
        style_filename = get_stylesheet(stylesheet)
        style = etree.parse(style_filename)

        document = copy.deepcopy(wldoc)
        del wldoc
        document.swap_endlines()

        if flags:
            for flag in flags:
                document.edoc.getroot().set(flag, 'yes')

        document.clean_ed_note()
        document.clean_ed_note('abstrakt')

        if not options:
            options = {}
        options.setdefault('gallery', "''")
        result = document.transform(style, **options)
        del document  # no longer needed large object :)

        if html_has_content(result):
            add_anchors(result.getroot())
            add_table_of_themes(result.getroot())
            add_table_of_contents(result.getroot())

            return OutputFile.from_string(etree.tostring(
                result, method='html', xml_declaration=False, pretty_print=True, encoding='utf-8'))
        else:
            return None
    except KeyError:
        raise ValueError("'%s' is not a valid stylesheet.")
    except (XMLSyntaxError, XSLTApplyError), e:
        raise ParseError(e)


class Fragment(object):
    def __init__(self, id, themes):
        super(Fragment, self).__init__()
        self.id = id
        self.themes = themes
        self.events = []

    def append(self, event, element):
        self.events.append((event, element))

    def closed_events(self):
        stack = []
        for event, element in self.events:
            if event == 'start':
                stack.append(('end', element))
            elif event == 'end':
                try:
                    stack.pop()
                except IndexError:
                    print 'CLOSED NON-OPEN TAG:', element

        stack.reverse()
        return self.events + stack

    def to_string(self):
        result = []
        for event, element in self.closed_events():
            if event == 'start':
                result.append(u'<%s %s>' % (
                    element.tag, ' '.join('%s="%s"' % (k, v) for k, v in element.attrib.items())))
                if element.text:
                    result.append(element.text)
            elif event == 'end':
                result.append(u'</%s>' % element.tag)
                if element.tail:
                    result.append(element.tail)
            else:
                result.append(element)

        return ''.join(result)

    def __unicode__(self):
        return self.to_string()


def extract_fragments(input_filename):
    """Extracts theme fragments from input_filename."""
    open_fragments = {}
    closed_fragments = {}

    # iterparse would die on a HTML document
    parser = etree.HTMLParser(encoding='utf-8')
    buf = cStringIO.StringIO()
    buf.write(etree.tostring(etree.parse(input_filename, parser).getroot()[0][0], encoding='utf-8'))
    buf.seek(0)

    for event, element in etree.iterparse(buf, events=('start', 'end')):
        # Process begin and end elements
        if element.get('class', '') in ('theme-begin', 'theme-end'):
            if not event == 'end':
                continue  # Process elements only once, on end event

            # Open new fragment
            if element.get('class', '') == 'theme-begin':
                fragment = Fragment(id=element.get('fid'), themes=element.text)

                # Append parents
                parent = element.getparent()
                parents = []
                while parent.get('id', None) != 'book-text':
                    cparent = copy.deepcopy(parent)
                    cparent.text = None
                    parents.append(cparent)
                    parent = parent.getparent()

                parents.reverse()
                for parent in parents:
                    fragment.append('start', parent)

                open_fragments[fragment.id] = fragment

            # Close existing fragment
            else:
                try:
                    fragment = open_fragments[element.get('fid')]
                except KeyError:
                    print '%s:closed not open fragment #%s' % (input_filename, element.get('fid'))
                else:
                    closed_fragments[fragment.id] = fragment
                    del open_fragments[fragment.id]

            # Append element tail to lost_text (we don't want to lose any text)
            if element.tail:
                for fragment_id in open_fragments:
                    open_fragments[fragment_id].append('text', element.tail)

        # Process all elements except begin and end
        else:
            # Omit annotation tags
            if (len(element.get('name', '')) or 
                    element.get('class', '') in ('annotation', 'anchor')):
                if event == 'end' and element.tail:
                    for fragment_id in open_fragments:
                        open_fragments[fragment_id].append('text', element.tail)
            else:
                for fragment_id in open_fragments:
                    open_fragments[fragment_id].append(event, copy.copy(element))

    return closed_fragments, open_fragments


def add_anchor(element, prefix, with_link=True, with_target=True, link_text=None):
    parent = element.getparent()
    index = parent.index(element)

    if with_link:
        if link_text is None:
            link_text = prefix
        anchor = etree.Element('a', href='#%s' % prefix)
        anchor.set('class', 'anchor')
        anchor.text = unicode(link_text)
        parent.insert(index, anchor)

    if with_target:
        anchor_target = etree.Element('a', name='%s' % prefix)
        anchor_target.set('class', 'target')
        anchor_target.text = u' '
        parent.insert(index, anchor_target)


def any_ancestor(element, test):
    for ancestor in element.iterancestors():
        if test(ancestor):
            return True
    return False


def add_anchors(root):
    counter = 1
    for element in root.iterdescendants():
        def f(e):
            return e.get('class') in ('note', 'motto', 'motto_podpis', 'dedication') or \
                e.get('id') == 'nota_red' or e.tag == 'blockquote'
        if any_ancestor(element, f):
            continue

        if element.tag == 'p' and 'verse' in element.get('class', ''):
            if counter == 1 or counter % 5 == 0:
                add_anchor(element, "f%d" % counter, link_text=counter)
            counter += 1
        elif 'paragraph' in element.get('class', ''):
            add_anchor(element, "f%d" % counter, link_text=counter)
            counter += 1


def raw_printable_text(element):
    working = copy.deepcopy(element)
    for e in working.findall('a'):
        if e.get('class') in ('annotation', 'theme-begin'):
            e.text = ''
    return etree.tostring(working, method='text', encoding=unicode).strip()


def add_table_of_contents(root):
    sections = []
    counter = 1
    for element in root.iterdescendants():
        if element.tag in ('h2', 'h3'):
            if any_ancestor(element,
                            lambda e: e.get('id') in ('footnotes', 'nota_red') or e.get('class') in ('person-list',)):
                continue

            element_text = raw_printable_text(element)
            if element.tag == 'h3' and len(sections) and sections[-1][1] == 'h2':
                sections[-1][3].append((counter, element.tag, element_text, []))
            else:
                sections.append((counter, element.tag, element_text, []))
            add_anchor(element, "s%d" % counter, with_link=False)
            counter += 1

    toc = etree.Element('div')
    toc.set('id', 'toc')
    toc_header = etree.SubElement(toc, 'h2')
    toc_header.text = u'Spis treści'
    toc_list = etree.SubElement(toc, 'ol')

    for n, section, text, subsections in sections:
        section_element = etree.SubElement(toc_list, 'li')
        add_anchor(section_element, "s%d" % n, with_target=False, link_text=text)

        if len(subsections):
            subsection_list = etree.SubElement(section_element, 'ol')
            for n1, subsection, subtext, _ in subsections:
                subsection_element = etree.SubElement(subsection_list, 'li')
                add_anchor(subsection_element, "s%d" % n1, with_target=False, link_text=subtext)

    root.insert(0, toc)

    
def add_table_of_themes(root):
    try:
        from sortify import sortify
    except ImportError:
        def sortify(x):
            return x

    book_themes = {}
    for fragment in root.findall('.//a[@class="theme-begin"]'):
        if not fragment.text:
            continue
        theme_names = [s.strip() for s in fragment.text.split(',')]
        for theme_name in theme_names:
            book_themes.setdefault(theme_name, []).append(fragment.get('name'))
    book_themes = book_themes.items()
    book_themes.sort(key=lambda s: sortify(s[0]))
    themes_div = etree.Element('div', id="themes")
    themes_ol = etree.SubElement(themes_div, 'ol')
    for theme_name, fragments in book_themes:
        themes_li = etree.SubElement(themes_ol, 'li')
        themes_li.text = "%s: " % theme_name
        for i, fragment in enumerate(fragments):
            item = etree.SubElement(themes_li, 'a', href="#%s" % fragment)
            item.text = str(i + 1)
            item.tail = ' '
    root.insert(0, themes_div)


def extract_annotations(html_path):
    """Extracts annotations from HTML for annotations dictionary.

    For each annotation, yields a tuple of:
    anchor, footnote type, valid qualifiers, text, html.

    """
    from .fn_qualifiers import FN_QUALIFIERS

    parser = etree.HTMLParser(encoding='utf-8')
    tree = etree.parse(html_path, parser)
    footnotes = tree.find('//*[@id="footnotes"]')
    re_qualifier = re.compile(ur'[^\u2014]+\s+\(([^\)]+)\)\s+\u2014')
    if footnotes is not None:
        for footnote in footnotes.findall('div'):
            fn_type = footnote.get('class').split('-')[1]
            anchor = footnote.find('a[@class="annotation"]').get('href')[1:]
            del footnote[:2]
            footnote.text = None
            if len(footnote) and footnote[-1].tail == '\n':
                footnote[-1].tail = None
            text_str = etree.tostring(footnote, method='text', encoding=unicode).strip()
            html_str = etree.tostring(footnote, method='html', encoding=unicode).strip()

            match = re_qualifier.match(text_str)
            if match:
                qualifier_str = match.group(1)
                qualifiers = []
                for candidate in re.split('[;,]', qualifier_str):
                    candidate = candidate.strip()
                    if candidate in FN_QUALIFIERS:
                        qualifiers.append(candidate)
                    elif candidate.startswith('z '):
                        subcandidate = candidate.split()[1]
                        if subcandidate in FN_QUALIFIERS:
                            qualifiers.append(subcandidate)
            else:
                qualifiers = []

            yield anchor, fn_type, qualifiers, text_str, html_str
