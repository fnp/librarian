# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.  
#
from librarian import dcparser, parser
from lxml import etree
import cStringIO
import codecs
import os
import re


ENTITY_SUBSTITUTIONS = [
    (u'---', u'—'),
    (u'--', u'–'),
    (u'...', u'…'),
    (u',,', u'„'),
    (u'"', u'”'),
]


TEMPLATE = u"""\
Kodowanie znaków w dokumencie: UTF-8.
-----
Publikacja zrealizowana w ramach projektu Wolne Lektury (http://wolnelektury.pl/). Reprodukcja cyfrowa wykonana przez
Bibliotekę Narodową z egzemplarza pochodzącego ze zbiorów BN. Ten utwór nie jest chroniony prawem autorskim i znajduje
się w domenie publicznej, co oznacza, że możesz go swobodnie wykorzystywać, publikować i rozpowszechniać.

Wersja lektury w opracowaniu merytorycznym i krytycznym (przypisy i motywy) dostępna jest na stronie %(url)s.
-----



%(text)s
"""


def strip(context, text):
    """Remove unneeded whitespace from beginning and end"""
    if isinstance(text, list):
        text = ''.join(text)
    return re.sub(r'\s+', ' ', text).strip()


def substitute_entities(context, text):
    """XPath extension function converting all entites in passed text."""
    if isinstance(text, list):
        text = ''.join(text)
    for entity, substitutution in ENTITY_SUBSTITUTIONS:
        text = text.replace(entity, substitutution)
    return text


def wrap_words(context, text, wrapping):
    """XPath extension function automatically wrapping words in passed text"""
    if isinstance(text, list):
        text = ''.join(text)
    if not wrapping:
        return text
    
    words = re.split(r'\s', text)
    
    line_length = 0
    lines = [[]]
    for word in words:
        line_length += len(word) + 1
        if line_length > wrapping:
            # Max line length was exceeded. We create new line
            lines.append([])
            line_length = len(word)
        lines[-1].append(word)
    return '\n'.join(' '.join(line) for line in lines)


# Register substitute_entities function with lxml
ns = etree.FunctionNamespace('http://wolnelektury.pl/functions')
ns['strip'] = strip
ns['substitute_entities'] = substitute_entities
ns['wrap_words'] = wrap_words


def transform(input_filename, output_filename, is_file=True, parse_dublincore=True, **options):
    """Transforms file input_filename in XML to output_filename in TXT."""
    # Parse XSLT
    style_filename = os.path.join(os.path.dirname(__file__), 'xslt/book2txt.xslt')
    style = etree.parse(style_filename)

    if is_file:
        document = parser.WLDocument.from_file(input_filename, True, parse_dublincore=parse_dublincore)
    else:
        document = parser.WLDocument.from_string(input_filename, True, parse_dublincore=parse_dublincore)

    result = document.transform(style, **options)

    output_file = codecs.open(output_filename, 'wb', encoding='utf-8')
    
    if parse_dublincore:
        url = dcparser.parse(input_filename).url
    else:
        url = '*' * 10
    output_file.write(TEMPLATE % {
        'url': url,
        'text': unicode(result),
    })

