# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from lxml import etree
import re
from ebooklib import epub

from librarian.dcparser import Person
from librarian import get_resource


def _register_function(f):
    """ Register extension function with lxml """
    ns = etree.FunctionNamespace('http://wolnelektury.pl/functions')
    ns[f.__name__] = f


def reg_substitute_entities():
    entity_substitutions = [
        ('---', '—'),
        ('--', '–'),
        ('...', '…'),
        (',,', '„'),
        ('"', '”'),
    ]

    def substitute_entities(context, text):
        """XPath extension function converting all entites in passed text."""
        if isinstance(text, list):
            text = ''.join(text)
        for entity, substitutution in entity_substitutions:
            text = text.replace(entity, substitutution)
        return text

    _register_function(substitute_entities)


def reg_strip():
    def strip(context, text):
        """Remove unneeded whitespace from beginning and end"""
        if isinstance(text, list):
            text = ''.join(text)
        return re.sub(r'\s+', ' ', text).strip()
    _register_function(strip)


def reg_starts_white():
    def starts_white(context, text):
        if isinstance(text, list):
            text = ''.join(text)
        if not text:
            return False
        return text[0].isspace()
    _register_function(starts_white)


def reg_ends_white():
    def ends_white(context, text):
        if isinstance(text, list):
            text = ''.join(text)
        if not text:
            return False
        return text[-1].isspace()
    _register_function(ends_white)


def reg_person_name():
    def person_name(context, text):
        """ Converts "Name, Forename" to "Forename Name" """
        if isinstance(text, list):
            text = ''.join(text)
        return Person.from_text(text).readable()
    _register_function(person_name)


def reg_texcommand():
    def texcommand(context, text):
        """Remove non-letters"""
        if isinstance(text, list):
            text = ''.join(text)
        return re.sub(r'[^a-zA-Z]', '', text).strip()
    _register_function(texcommand)


def lang_code_3to2(text):
    """Convert 3-letter language code to 2-letter code"""
    result = ''
    text = ''.join(text)
    with open(get_resource('res/ISO-639-2_8859-1.txt'), 'rb') as f:
        for line in f.read().decode('latin1').split('\n'):
            codes = line.strip().split('|')
            if codes[0] == text:
                result = codes[2]
    if result == '':
        return text
    else:
        return result


def mathml_latex(context, trees):
    from librarian.embeds.mathml import MathML
    text = MathML(trees[0]).to_latex().data
    # Remove invisible multiplications, they produce unwanted spaces.
    text = text.replace('\u2062', '')
    return text


def reg_mathml_latex():
    _register_function(mathml_latex)


def reg_mathml_epub(output):
    from librarian.embeds.mathml import MathML

    def mathml(context, trees):
        data = MathML(trees[0]).to_latex().to_png().data
        name = "math%d.png" % mathml.count
        mathml.count += 1
        output.add_item(
            epub.EpubItem(
                uid='math%d' % mathml.count,
                file_name=name,
                media_type='image/png',
                content=data
            )
        )

        return name
    mathml.count = 0
    _register_function(mathml)
