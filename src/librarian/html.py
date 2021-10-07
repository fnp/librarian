# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from __future__ import print_function, unicode_literals

import os
import re
import copy

from lxml import etree
from librarian import XHTMLNS, ParseError, OutputFile
from librarian import functions
from PIL import Image

from lxml.etree import XMLSyntaxError, XSLTApplyError
import six


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
    return etree.ETXPath(
        '//p|//{%(ns)s}p|//h1|//{%(ns)s}h1' % {'ns': str(XHTMLNS)}
    )(text)


def transform_abstrakt(abstrakt_element):
    style_filename = get_stylesheet('legacy')
    style = etree.parse(style_filename)
    xml = etree.tostring(abstrakt_element, encoding='unicode')
    document = etree.parse(six.StringIO(
        xml.replace('abstrakt', 'dlugi_cytat')
    ))  # HACK
    result = document.xslt(style)
    html = re.sub('<a name="sec[0-9]*"/>', '',
                  etree.tostring(result, encoding='unicode'))
    return re.sub('</?blockquote[^>]*>', '', html)


def add_image_sizes(tree, gallery_path, gallery_url, base_url):
    widths = [360, 600, 1200, 1800, 2400]

    for i, ilustr in enumerate(tree.findall('//ilustr')):
        rel_path = ilustr.attrib['src']
        img_url = six.moves.urllib.parse.urljoin(base_url, rel_path)

        f = six.moves.urllib.request.urlopen(img_url)
        img = Image.open(f)
        ext = {'GIF': 'gif', 'PNG': 'png'}.get(img.format, 'jpg')

        srcset = []
        # Needed widths: predefined and original, limited by
        # whichever is smaller.
        img_widths = [
            w for w in
            sorted(
                set(widths + [img.size[0]])
            )
            if w <= min(widths[-1], img.size[0])
        ]
        largest = None
        for w in widths:
            fname = '%d.W%d.%s' % (i, w, ext)
            fpath = gallery_path + fname
            if not os.path.exists(fpath):
                height = round(img.size[1] * w / img.size[0])
                th = img.resize((w, height))
                th.save(fpath)
            th_url = gallery_url + fname
            srcset.append(" ".join((
                th_url,
                '%dw' % w
            )))
            largest_url = th_url
        ilustr.attrib['srcset'] = ", ".join(srcset)
        ilustr.attrib['src'] = largest_url

        f.close()


def transform(wldoc, stylesheet='legacy', options=None, flags=None, css=None, gallery_path='img/', gallery_url='img/', base_url='file://./'):
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
        document.fix_pa_akap()
        
        if not options:
            options = {}

        try:
            os.makedirs(gallery_path)
        except OSError:
            pass

        add_image_sizes(document.edoc, gallery_path, gallery_url, base_url)

        css = (
            css
            or 'https://static.wolnelektury.pl/css/compressed/book_text.css'
        )
        css = "'%s'" % css
        result = document.transform(style, css=css, **options)
        del document  # no longer needed large object :)

        if html_has_content(result):
            add_anchors(result.getroot())
            add_table_of_themes(result.getroot())
            add_table_of_contents(result.getroot())

            return OutputFile.from_bytes(etree.tostring(
                result, method='html', xml_declaration=False,
                pretty_print=True, encoding='utf-8'
            ))
        else:
            return None
    except KeyError:
        raise ValueError("'%s' is not a valid stylesheet.")
    except (XMLSyntaxError, XSLTApplyError) as e:
        raise ParseError(e)


@six.python_2_unicode_compatible
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
                    print('CLOSED NON-OPEN TAG:', element)

        stack.reverse()
        return self.events + stack

    def to_string(self):
        result = []
        for event, element in self.closed_events():
            if event == 'start':
                result.append(u'<%s %s>' % (
                    element.tag,
                    ' '.join(
                        '%s="%s"' % (k, v)
                        for k, v in element.attrib.items()
                    )
                ))
                if element.text:
                    result.append(element.text)
            elif event == 'end':
                result.append(u'</%s>' % element.tag)
                if element.tail:
                    result.append(element.tail)
            else:
                result.append(element)

        return ''.join(result)

    def __str__(self):
        return self.to_string()


def extract_fragments(input_filename):
    """Extracts theme fragments from input_filename."""
    open_fragments = {}
    closed_fragments = {}

    # iterparse would die on a HTML document
    parser = etree.HTMLParser(encoding='utf-8')
    buf = six.BytesIO()
    buf.write(etree.tostring(
        etree.parse(input_filename, parser).getroot()[0][0],
        encoding='utf-8'
    ))
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
                    if 'id' in cparent.attrib:
                        del cparent.attrib['id']
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
                    print('%s:closed not open fragment #%s' % (
                        input_filename, element.get('fid')
                    ))
                else:
                    closed_fragments[fragment.id] = fragment
                    del open_fragments[fragment.id]

            # Append element tail to lost_text
            # (we don't want to lose any text)
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
                        open_fragments[fragment_id].append(
                            'text', element.tail
                        )
            else:
                for fragment_id in open_fragments:
                    celem = copy.copy(element)
                    if 'id' in celem.attrib:
                        del celem.attrib['id']
                    open_fragments[fragment_id].append(
                        event, celem
                    )

    return closed_fragments, open_fragments


def add_anchor(element, prefix, with_link=True, with_target=True,
               link_text=None):
    parent = element.getparent()
    index = parent.index(element)

    if with_link:
        if link_text is None:
            link_text = prefix
        anchor = etree.Element('a', href='#%s' % prefix)
        anchor.set('class', 'anchor')
        anchor.text = six.text_type(link_text)
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
            return (
                e.get('class') in (
                    'note', 'motto', 'motto_podpis', 'dedication', 'frame'
                )
                or e.get('id') == 'nota_red'
                or e.tag == 'blockquote'
                or e.get('id') == 'footnotes'
            )
        if any_ancestor(element, f):
            continue

        if element.tag == 'div' and 'verse' in element.get('class', ''):
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
    return etree.tostring(working, method='text', encoding='unicode').strip()


def add_table_of_contents(root):
    sections = []
    counter = 1
    for element in root.iterdescendants():
        if element.tag in ('h2', 'h3'):
            if any_ancestor(
                    element,
                    lambda e: e.get('id') in (
                        'footnotes', 'nota_red'
                    ) or e.get('class') in ('person-list',)):
                continue

            element_text = raw_printable_text(element)
            if (element.tag == 'h3' and len(sections)
                    and sections[-1][1] == 'h2'):
                sections[-1][3].append(
                    (counter, element.tag, element_text, [])
                )
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
        add_anchor(section_element, "s%d" % n, with_target=False,
                   link_text=text)

        if len(subsections):
            subsection_list = etree.SubElement(section_element, 'ol')
            for n1, subsection, subtext, _ in subsections:
                subsection_element = etree.SubElement(subsection_list, 'li')
                add_anchor(subsection_element, "s%d" % n1, with_target=False,
                           link_text=subtext)

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
    book_themes = list(book_themes.items())
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
    re_qualifier = re.compile(r'[^\u2014]+\s+\(([^\)]+)\)\s+\u2014')
    if footnotes is not None:
        for footnote in footnotes.findall('div'):
            fn_type = footnote.get('class').split('-')[1]
            anchor = footnote.find('a[@class="annotation"]').get('href')[1:]
            del footnote[:2]
            footnote.text = None
            if len(footnote) and footnote[-1].tail == '\n':
                footnote[-1].tail = None
            text_str = etree.tostring(footnote, method='text',
                                      encoding='unicode').strip()
            html_str = etree.tostring(footnote, method='html',
                                      encoding='unicode').strip()

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
