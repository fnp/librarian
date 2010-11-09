# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from librarian import dcparser, parser, functions
from lxml import etree
import cStringIO
import codecs
import os
import re


functions.reg_substitute_entities()
functions.reg_wrap_words()
functions.reg_strip()

TEMPLATE = u"""\
Kodowanie znaków w dokumencie: UTF-8.
-----
Publikacja zrealizowana w ramach projektu Wolne Lektury (http://wolnelektury.pl/). Reprodukcja cyfrowa wykonana przez
Bibliotekę Narodową z egzemplarza pochodzącego ze zbiorów BN. 
\n%(license_description)s.

Wersja lektury w opracowaniu merytorycznym i krytycznym (przypisy i motywy) dostępna jest na stronie %(url)s.
-----



%(text)s
"""

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
        parsed_dc = dcparser.parse(input_filename)
        url = parsed_dc.url
        license_description = parsed_dc.license_description
	license = parsed_dc.license
        if license:
            license_description = u"Ten utwór jest udostepniony na licencji %s: \n%s" % (license_description, license)        
        else:
            license_description = u"Ten utwór nie jest chroniony prawem autorskim i znajduje się w domenie publicznej, co oznacza, że możesz go swobodnie wykorzystywać, publikować i rozpowszechniać" 
    else:
        url = '*' * 10
        license = ""
        license_description = ""
    output_file.write(TEMPLATE % {
        'url': url,
	'license_description': license_description,
        'text': unicode(result),
    })

