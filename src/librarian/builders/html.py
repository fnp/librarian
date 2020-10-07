# coding: utf-8
from __future__ import unicode_literals

from lxml import etree
from librarian.html import add_anchors, add_table_of_contents, add_table_of_themes
from librarian import OutputFile


class HtmlBuilder:
    file_extension = "html"
    identifier = "html"

    def __init__(self, image_location='https://wolnelektury.pl/media/book/pictures/marcos-historia-kolorow/'):
        self.image_location = image_location

        self.tree = text = etree.Element('div', **{'id': 'book-text'})
        self.header = etree.SubElement(text, 'h1')

        self.footnotes = etree.Element('div', id='footnotes')
        self.footnote_counter = 0

        self.nota_red = etree.Element('div', id='nota_red')

        self.cursors = {
            None: text,
            'header': self.header,
            'footnotes': self.footnotes,
            'nota_red': self.nota_red,
        }
        self.current_cursors = [None]

    @property
    def cursor(self):
        return self.cursors[self.current_cursors[-1]]

    @cursor.setter
    def cursor(self, value):
        self.cursors[self.current_cursors[-1]] = value

    def enter_fragment(self, fragment):
        self.current_cursors.append(fragment)

    def exit_fragment(self):
        self.current_cursors.pop()

    def create_fragment(self, name, element):
        assert name not in self.cursors
        self.cursors[name] = element

    def forget_fragment(self, name):
        del self.cursors[name]

    def preprocess(self, document):
        document._compat_assign_ordered_ids()
        document._compat_assign_section_ids()

    def build(self, document):
        self.preprocess(document)
        document.tree.getroot().html_build(self)
        self.postprocess(document)

        return OutputFile.from_bytes(
            etree.tostring(
                self.tree,
                method='html',
                encoding='utf-8',
                pretty_print=True
            )
        )

    def postprocess(self, document):
        _ = document.tree.getroot().master.gettext

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

        add_anchors(self.tree)
        if len(self.nota_red):
            self.tree.append(self.nota_red)
        add_table_of_themes(self.tree)
        add_table_of_contents(self.tree)

        if self.footnote_counter:
            fnheader = etree.Element("h3")
            fnheader.text = _("Footnotes")
            self.footnotes.insert(0, fnheader)
            self.tree.append(self.footnotes)

    def start_element(self, tag, attrib=None):
        self.cursor = etree.SubElement(
            self.cursor,
            tag,
            **(attrib or {})
        )

    def end_element(self):
        self.cursor = self.cursor.getparent()

    def push_text(self, text):
        if text == 'Między nami nic nie było':
            print(self.cursors)
            print(self.current_cursors)
        cursor = self.cursor
        if len(cursor):
            cursor[-1].tail = (cursor[-1].tail or '') + text
        else:
            cursor.text = (cursor.text or '') + text


class StandaloneHtmlBuilder(HtmlBuilder):
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

        etree.SubElement(
            head,
            'link',
            href="https://static.wolnelektury.pl/css/compressed/book_text.css",
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
