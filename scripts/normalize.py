# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from __future__ import with_statement

import re
import sys
import os.path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from StringIO import StringIO
from lxml import etree
import librarian

REPLACEMENTS = (
    (u'---', u'\u2014'), # mdash
    (u'--', u'\u2013'),  # ndash
    (u'...', u'\u2026'), # ldots
    (u',,', u'\u201E'),  # lower double back-quote
    (u'"', u'\u201D'),   # upper double quote
)

DIALOG_EXPR = re.compile(r"\s*---\s(.*)")

def wl_normalize_text(context, text):
    """XPath extension function converting all entites in passed text."""
    if isinstance(text, list):
        text = u''.join(text)

    for code, ucode in REPLACEMENTS:
        text = text.replace(code, ucode)

    return text

def wl_fix_dialog(context, data):

    if isinstance(data, list):
        text = u''.join(data)
    else:
        text = data

    m = DIALOG_EXPR.match(text)

    if m is not None:
        return m.group(1)
    else:
        return text


def filter_verse_ends(data):
    return data.replace('/\n', '<br />')

ns = etree.FunctionNamespace('http://wolnelektury.pl/functions')
ns['normalize-text'] = wl_normalize_text
ns['fix-dialog-line'] = wl_fix_dialog

def normalize_stylesheet():
    return etree.XSLT(etree.parse(os.path.join(os.path.dirname(librarian.__file__), 'xslt', 'normalize.xslt')))

if __name__ == '__main__':
    tran = normalize_stylesheet()
    input = StringIO( f )
    doc = trans( etree.parse(input) )
    print etree.tostring(doc, pretty_print=True, encoding=unicode).encode('utf-8')

    for err in trans.error_log:
        sys.stderr.write( (u"%s\n" % err).encode('utf-8') )

