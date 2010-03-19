# -*- coding: utf-8 -*-
import os
import cStringIO
import re
import codecs

from lxml import etree

from librarian import dcparser


ENTITY_SUBSTITUTIONS = [
    (u'---', u'—'),
    (u'--', u'–'),
    (u'...', u'…'),
    (u',,', u'„'),
    (u'"', u'”'),
]


MAX_LINE_LENGTH = 80


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


def wrap_words(context, text):
    """XPath extension function automatically wrapping words in passed text"""
    if isinstance(text, list):
        text = ''.join(text)
    words = re.split(r'\s', text)
    
    line_length = 0
    lines = [[]]
    for word in words:
        line_length += len(word) + 1
        if line_length > MAX_LINE_LENGTH:
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


def transform(input_filename, output_filename):
    """Transforms file input_filename in XML to output_filename in TXT."""
    # Parse XSLT
    style_filename = os.path.join(os.path.dirname(__file__), 'book2txt.xslt')
    style = etree.parse(style_filename)

    doc_file = cStringIO.StringIO()
    expr = re.compile(r'/\s', re.MULTILINE | re.UNICODE);
    
    f = open(input_filename, 'r')
    for line in f:
        line = line.decode('utf-8')
        line = expr.sub(u'<br/>\n', line)
        doc_file.write(line.encode('utf-8'))
    f.close()

    doc_file.seek(0)

    parser = etree.XMLParser(remove_blank_text=True)
    doc = etree.parse(doc_file, parser)
    
    result = doc.xslt(style)
    output_file = codecs.open(output_filename, 'wb', encoding='utf-8')
    output_file.write(unicode(result) % dcparser.parse(input_filename).url)

