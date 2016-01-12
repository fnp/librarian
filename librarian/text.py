# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import copy
from librarian import functions, OutputFile
from lxml import etree
import os


functions.reg_substitute_entities()
functions.reg_wrap_words()
functions.reg_strip()
functions.reg_person_name()

TEMPLATE = u"""\
%(text)s


-----
Ta lektura, podobnie jak tysiące innych, dostępna jest na stronie wolnelektury.pl.
Wersja lektury w opracowaniu merytorycznym i krytycznym (przypisy i motywy) dostępna jest na stronie %(url)s.

Utwór opracowany został w ramach projektu Wolne Lektury przez fundację Nowoczesna Polska.

%(license_description)s.%(source)s

%(description)s%(contributors)s%(funders)s
"""


def transform(wldoc, flags=None, **options):
    """
    Transforms input_file in XML to output_file in TXT.
    possible flags: raw-text,
    """
    # Parse XSLT
    style_filename = os.path.join(os.path.dirname(__file__), 'xslt/book2txt.xslt')
    style = etree.parse(style_filename)

    document = copy.deepcopy(wldoc)
    del wldoc
    document.swap_endlines()

    if flags:
        for flag in flags:
            document.edoc.getroot().set(flag, 'yes')
    if 'wrapping' in options:
        options['wrapping'] = str(options['wrapping'])

    result = document.transform(style, **options)

    if not flags or 'raw-text' not in flags:
        if document.book_info:
            parsed_dc = document.book_info
            description = parsed_dc.description
            url = document.book_info.url
    
            license_description = parsed_dc.license_description
            license = parsed_dc.license
            if license:
                license_description = u"Ten utwór jest udostepniony na licencji %s: \n%s" % (
                    license_description, license)
            else:
                license_description = u"Ten utwór nie jest objęty majątkowym prawem autorskim i znajduje się " \
                                      u"w domenie publicznej, co oznacza że możesz go swobodnie wykorzystywać, " \
                                      u"publikować i rozpowszechniać. Jeśli utwór opatrzony jest dodatkowymi " \
                                      u"materiałami (przypisy, motywy literackie etc.), które podlegają prawu " \
                                      u"autorskiemu, to te dodatkowe materiały udostępnione są na licencji " \
                                      u"Creative Commons Uznanie Autorstwa – Na Tych Samych Warunkach 3.0 PL " \
                                      u"(http://creativecommons.org/licenses/by-sa/3.0/)"

            source = parsed_dc.source_name
            if source:
                source = "\n\nTekst opracowany na podstawie: " + source
            else:
                source = ''
    
            contributors = ', '.join(person.readable() for person in 
                                     sorted(set(p for p in (parsed_dc.technical_editors + parsed_dc.editors) if p)))
            if contributors:
                contributors = "\n\nOpracowanie redakcyjne i przypisy: %s." % contributors
            funders = ', '.join(parsed_dc.funders)
            if funders:
                funders = u"\n\nPublikację ufundowali i ufundowały: %s." % funders
        else:
            description = 'Publikacja zrealizowana w ramach projektu Wolne Lektury (http://wolnelektury.pl).'
            url = '*' * 10
            license_description = ""
            source = ""
            contributors = ""
            funders = ""
        result = (TEMPLATE % {
            'description': description,
            'url': url,
            'license_description': license_description,
            'text': unicode(result),
            'source': source,
            'contributors': contributors,
            'funders': funders,
        }).encode('utf-8')
    else:
        result = unicode(result).encode('utf-8')
    return OutputFile.from_string("\r\n".join(result.splitlines()) + "\r\n")
