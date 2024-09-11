# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from collections import defaultdict
import os
from urllib.request import urlopen
from lxml import etree
from librarian.html import add_table_of_contents, add_table_of_themes, add_image_sizes
from librarian import OutputFile


class HtmlBuilder:
    file_extension = "html"
    with_themes = True
    with_toc = True
    with_footnotes = True
    with_nota_red = True
    with_ids = True
    with_numbering = True
    no_externalities = False
    orphans = True

    root_tag = 'div'
    root_attrib = {'id': 'book-text'}

    def __init__(self, gallery_path=None, gallery_url=None, base_url=None):
        self._base_url = base_url
        self.gallery_path = gallery_path
        self.gallery_url = gallery_url

        self.tree = text = etree.Element(self.root_tag, **self.root_attrib)
        self.header = etree.Element('h1')

        self.footnotes = etree.Element('div', id='footnotes')
        self.counters = defaultdict(lambda: 1)

        self.nota_red = etree.Element('div', id='nota_red')

        self.cursors = {
            None: text,
            'header': self.header,
            'footnotes': self.footnotes,
            'nota_red': self.nota_red,
        }
        self.current_cursors = [text]

    @property
    def base_url(self):
        if self._base_url is not None:
            return self._base_url
        else:
            return 'https://wolnelektury.pl/media/book/pictures/{}/'.format(self.document.meta.url.slug)

    @property
    def cursor(self):
        return self.current_cursors[-1]

    def enter_fragment(self, fragment):
        cursor = self.cursors.get(fragment, self.cursor)
        self.current_cursors.append(cursor)

    def exit_fragment(self):
        self.current_cursors.pop()

    def create_fragment(self, name, element):
        assert name not in self.cursors
        self.cursors[name] = element

    def forget_fragment(self, name):
        del self.cursors[name]

    def build(self, document, element=None, **kwargs):
        self.document = document

        self.assign_ids(self.document.tree)
        self.prepare_images()

        if element is None:
            element = document.tree.getroot()

        element.html_build(self)
        self.postprocess(document)
        return self.output()

    def assign_ids(self, tree):
        # Assign IDs depth-first, to account for any <numeracja> inside.
        for _e, elem in etree.iterwalk(tree, events=('end',)):
            if getattr(elem, 'NUMBERING', None):
                elem.assign_id(self)

    def prepare_images(self):
        # Temporarily use the legacy method, before transitioning to external generators.
        if self.gallery_path is None:
            return
        try:
            os.makedirs(self.gallery_path)
        except OSError:
            pass
        add_image_sizes(self.document.tree, self.gallery_path, self.gallery_url, self.base_url)

    def output(self):
        if not len(self.tree):
            return None
        return OutputFile.from_bytes(
            etree.tostring(
                self.tree,
                method='html',
                encoding='utf-8',
                pretty_print=True
            )
        )

    def postprocess(self, document):
        _ = document.tree.getroot().gettext

        if document.meta.translators:
            self.enter_fragment('header')
            self.start_element('span', {'class': 'translator'})
            self.push_text(_("translated by") + " ")
            self.push_text(
                ", ".join(
                    translator.readable()
                    for translator in document.meta.translators
                )
            )
            self.exit_fragment()

        if len(self.header):
            self.tree.insert(0, self.header)
            
        if self.with_nota_red and len(self.nota_red):
            self.tree.append(self.nota_red)
        if self.with_themes:
            add_table_of_themes(self.tree)
        if self.with_toc:
            add_table_of_contents(self.tree)

        if self.counters['fn'] > 1:
            fnheader = etree.Element("h3")
            fnheader.text = _("Footnotes")
            self.footnotes.insert(0, fnheader)
            self.tree.append(self.footnotes)

    def start_element(self, tag, attrib=None):
        self.current_cursors.append(etree.SubElement(
            self.cursor,
            tag,
            **(attrib or {})
        ))

    def end_element(self):
        self.current_cursors.pop()

    def push_text(self, text):
        cursor = self.cursor
        if len(cursor):
            cursor[-1].tail = (cursor[-1].tail or '') + text
        else:
            cursor.text = (cursor.text or '') + text

    def add_visible_number(self, element):
        assert '_id' in element.attrib, etree.tostring(element)
        self.start_element('a', {
            'href': f'#{element.attrib["_id"]}',
            'class': 'wl-num',
        })
        self.push_text(element.attrib['_visible_numbering'])
        self.end_element()


class StandaloneHtmlBuilder(HtmlBuilder):
    css_url = "https://static.wolnelektury.pl/css/compressed/book_text.css"

    def postprocess(self, document):
        super(StandaloneHtmlBuilder, self).postprocess(document)

        tree = etree.Element('html')
        body = etree.SubElement(tree, 'body')
        body.append(self.tree)
        self.tree = tree

        head = etree.Element('head')
        tree.insert(0, head)

        etree.SubElement(head, 'meta', charset='utf-8')
        etree.SubElement(head, 'title').text = document.meta.title

        etree.SubElement(
            head,
            'meta',
            name="viewport",
            content="width=device-width, initial-scale=1, maximum-scale=1"
        )

        if self.no_externalities:
            etree.SubElement(
                head, 'style',
            ).text = urlopen(self.css_url).read().decode('utf-8')
        else:
            etree.SubElement(
                head,
                'link',
                href=self.css_url,
                rel="stylesheet",
                type="text/css",
            )

            etree.SubElement(
                body, 'script',
                src="https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"
            )

            etree.SubElement(
                body,
                "script",
                src="http://malsup.github.io/min/jquery.cycle2.min.js"
            )


class SnippetHtmlBuilder(HtmlBuilder):
    with_themes = False
    with_toc = False
    with_footnotes = False
    with_nota_red = False
    with_ids = False
    with_numbering = False


class AbstraktHtmlBuilder(HtmlBuilder):
    with_themes = False
    with_toc = False
    with_footnotes = False
    with_nota_red = False
    with_ids = False
    with_numbering = False

    root_tag = 'blockquote'
    root_attrib = {}

    def build(self, document, element=None, **kwargs):
        if element is None:
            element = document.tree.find('//abstrakt')
        element.attrib['_force'] = '1'
        return super().build(document, element, **kwargs)

            
class DaisyHtmlBuilder(StandaloneHtmlBuilder):
    file_extension = 'xhtml'
    with_themes = False
    with_toc = False
    with_footnotes = False
    with_nota_red = False
    with_deep_identifiers = False
    no_externalities = True
    with_numbering = False

    def output(self):
        tree = etree.ElementTree(self.tree)
        tree.docinfo.public_id = '-//W3C//DTD XHTML 1.0 Transitional//EN'
        tree.docinfo.system_url = 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'
        return OutputFile.from_bytes(
            etree.tostring(
                tree,
                encoding='utf-8',
                pretty_print=True,
                xml_declaration=True
            )
        )

