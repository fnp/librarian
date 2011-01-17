# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from librarian import dcparser, parser, functions
from lxml import etree
import os


functions.reg_substitute_entities()
functions.reg_wrap_words()
functions.reg_strip()

TEMPLATE = u"""\
Kodowanie znaków w dokumencie: UTF-8.
-----
%(description)s 

%(license_description)s.%(source)s

Wersja lektury w opracowaniu merytorycznym i krytycznym (przypisy i motywy) dostępna jest na stronie %(url)s.
-----



%(text)s
"""

def transform(input_file, output_file, parse_dublincore=True, **options):
    """Transforms input_file in XML to output_file in TXT."""
    # Parse XSLT
    style_filename = os.path.join(os.path.dirname(__file__), 'xslt/book2txt.xslt')
    style = etree.parse(style_filename)

    document = parser.WLDocument.from_file(input_file, True, parse_dublincore=parse_dublincore)
    result = document.transform(style, **options)

    if parse_dublincore:
        parsed_dc = dcparser.BookInfo.from_element(document.edoc)
        description = parsed_dc.description
        url = parsed_dc.url
        license_description = parsed_dc.license_description
        license = parsed_dc.license
        if license:
            license_description = u"Ten utwór jest udostepniony na licencji %s: \n%s" % (license_description, license)        
        else:
            license_description = u"Ten utwór nie jest chroniony prawem autorskim i znajduje się w domenie publicznej, co oznacza, że możesz go swobodnie wykorzystywać, publikować i rozpowszechniać"
        source = parsed_dc.source_name
        if source:
            source = "\n\nNa podstawie: " + source
        else:
            source = ''
    else:
        description = 'Publikacja zrealizowana w ramach projektu Wolne Lektury (http://wolnelektury.pl).'
        url = '*' * 10
        license = ""
        license_description = ""
        source = ""
    output_file.write((TEMPLATE % {
        'description': description,
        'url': url,
        'license_description': license_description,
        'text': unicode(result),
        'source': source,
    }).encode('utf-8'))

