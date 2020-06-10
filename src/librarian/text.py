# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from __future__ import unicode_literals

import copy
from librarian import functions, OutputFile, get_resource
from lxml import etree
import os
import six


functions.reg_substitute_entities()
functions.reg_wrap_words()
functions.reg_strip()
functions.reg_person_name()


with open(get_resource("res/text/template.txt")) as f:
    TEMPLATE = f.read()


def transform(wldoc, flags=None, **options):
    """
    Transforms input_file in XML to output_file in TXT.
    possible flags: raw-text,
    """
    # Parse XSLT
    style_filename = os.path.join(os.path.dirname(__file__),
                                  'xslt/book2txt.xslt')
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
                license_description = (
                    u"Ten utwór jest udostępniony na licencji %s: \n%s" % (
                        license_description, license
                    )
                )
            else:
                license_description = (
                    "Ten utwór nie jest objęty majątkowym prawem autorskim "
                    "i znajduje się w domenie publicznej, co oznacza że "
                    "możesz go swobodnie wykorzystywać, publikować "
                    "i rozpowszechniać. Jeśli utwór opatrzony jest "
                    "dodatkowymi materiałami (przypisy, motywy literackie "
                    "etc.), które podlegają prawu autorskiemu, to te "
                    "dodatkowe materiały udostępnione są na licencji "
                    "Creative Commons Uznanie Autorstwa – Na Tych Samych "
                    "Warunkach 3.0 PL "
                    "(http://creativecommons.org/licenses/by-sa/3.0/)"
                )

            source = parsed_dc.source_name
            if source:
                source = "\n\nTekst opracowany na podstawie: " + source
            else:
                source = ''

            contributors = ', '.join(
                person.readable()
                for person in sorted(set(
                    p for p in (
                        parsed_dc.technical_editors + parsed_dc.editors
                    ) if p))
            )
            if contributors:
                contributors = (
                    "\n\nOpracowanie redakcyjne i przypisy: %s."
                    % contributors
                )
            funders = ', '.join(parsed_dc.funders)
            if funders:
                funders = u"\n\nPublikację wsparli i wsparły: %s." % funders
            publisher = '\n\nWydawca: ' + ', '.join(parsed_dc.publisher)
            isbn = getattr(parsed_dc, 'isbn_txt', None)
            if isbn:
                isbn = '\n\n' + isbn
            else:
                isbn = ''
        else:
            description = ("Publikacja zrealizowana w ramach projektu "
                           "Wolne Lektury (http://wolnelektury.pl).")
            url = '*' * 10
            license_description = ""
            source = ""
            contributors = ""
            funders = ""
            publisher = ""
            isbn = ""
        result = (TEMPLATE % {
            'description': description,
            'url': url,
            'license_description': license_description,
            'text': six.text_type(result),
            'source': source,
            'contributors': contributors,
            'funders': funders,
            'publisher': publisher,
            'isbn': isbn,
        }).encode('utf-8')
    else:
        result = six.text_type(result).encode('utf-8')
    return OutputFile.from_bytes(b"\r\n".join(result.splitlines()) + b"\r\n")
