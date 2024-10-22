# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from lxml import etree
from librarian import FB2NS, XLINKNS, OutputFile
from .html import TreeBuilder


class FB2Builder(TreeBuilder):
    file_extension = 'fb2'
    build_method_fn = 'fb2_build'
    orphans = False
    
    def __init__(self, base_url=None):
        self.tree = etree.Element(
            FB2NS('FictionBook'),
            nsmap={
                None: FB2NS.uri,
                'l': XLINKNS.uri,
            }
        )
        description = etree.SubElement(self.tree, 'description')
        self.body = etree.SubElement(self.tree, 'body')
        self.header = etree.SubElement(self.body, 'title')
        self.epigraph = etree.SubElement(self.body, 'epigraph')
        self.text = etree.SubElement(self.body, 'section')

        self.footnotes = etree.Element(FB2NS('body'), name="notes")
        self.sections = []

        self.cursors = {
            None: self.text,
            'meta': description,
            'header': self.header,
            'epigraph': self.epigraph,
            'footnotes': self.footnotes,
            #'nota_red': self.nota_red,
        }
        self.current_cursors = [self.text]
        self.add_epigraph()

    def start_section(self, precedence):
        while self.sections and self.sections[-1] >= precedence:
            self.end_element()
            self.sections.pop()
        self.start_element('section')
        self.sections.append(precedence)

    def add_epigraph(self):
        self.enter_fragment('epigraph')
        self.start_element(FB2NS('p'))
        self.push_text('Utwór opracowany został w\xa0ramach projektu ')
        self.start_element(FB2NS('a'), {XLINKNS('href'): 'https://wolnelektury.pl/'})
        self.push_text('Wolne Lektury')
        self.end_element()
        self.push_text(' przez ')
        self.start_element(FB2NS('a'), {XLINKNS('href'): 'https://fundacja.wolnelektury.pl/'})
        self.push_text('fundację Wolne Lektury')
        self.end_element()
        self.push_text('.')
        self.end_element()
        self.exit_fragment()

    def add_meta(self, doc):
        self.enter_fragment('meta')

        self.start_element('title-info')

        self.start_element('genre')
        self.push_text('literature')
        self.end_element()
        for author in doc.meta.authors:
            self.start_element('author')
            self.simple_element('first-name', ' '.join(author.first_names))
            self.simple_element('last-name', author.last_name)
            self.end_element()
        self.simple_element('book-title', doc.meta.title)
        if doc.meta.released_to_public_domain_at:
            self.simple_element('date', doc.meta.released_to_public_domain_at)
        self.simple_element('lang', doc.meta.language)
        
        self.end_element()

        self.start_element('document-info')
        # contributor.editor
        # contributor.technical_editor
        self.simple_element('program-used', 'Wolne Lektury Librarian')
        self.simple_element('date', doc.meta.created_at)
        self.simple_element('id', str(doc.meta.url))
        self.simple_element('version', '0')
        
        self.end_element()
        self.start_element('publish-info')
        self.simple_element('publisher', '; '.join(doc.meta.publisher))
        self.end_element()
        self.exit_fragment()

    def build(self, doc, mp3=None):
        self.add_meta(doc)
        doc.tree.getroot().fb2_build(self)
        return self.output()

    def output(self):
        return OutputFile.from_bytes(
            etree.tostring(
                self.tree,
                encoding='utf-8',
                pretty_print=True,
                xml_declaration=True,
            )
        )




'''
import os.path
from copy import deepcopy
from lxml import etree

from librarian import functions, OutputFile
from .epub import replace_by_verse


functions.reg_substitute_entities()
functions.reg_person_name()


def sectionify(tree):
    """Finds section headers and adds a tree of _section tags."""
    sections = [
        'naglowek_czesc',
        'naglowek_akt', 'naglowek_rozdzial', 'naglowek_scena',
        'naglowek_podrozdzial']
    section_level = dict((v, k) for (k, v) in enumerate(sections))

    # We can assume there are just subelements an no text at section level.
    for level, section_name in reversed(list(enumerate(sections))):
        for header in tree.findall('//' + section_name):
            section = header.makeelement("_section")
            header.addprevious(section)
            section.append(header)
            sibling = section.getnext()
            while (sibling is not None and
                    section_level.get(sibling.tag, 1000) > level):
                section.append(sibling)
                sibling = section.getnext()


def transform(wldoc, verbose=False,
              cover=None, flags=None):
    document = deepcopy(wldoc)
    del wldoc

    if flags:
        for flag in flags:
            document.edoc.getroot().set(flag, 'yes')

    document.clean_ed_note()
    document.clean_ed_note('abstrakt')

    style_filename = os.path.join(os.path.dirname(__file__), 'fb2/fb2.xslt')
    style = etree.parse(style_filename)

    replace_by_verse(document.edoc)
    sectionify(document.edoc)

    result = document.transform(style)

    return OutputFile.from_bytes(str(result).encode('utf-8'))

# vim:et
'''
