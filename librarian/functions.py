# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from lxml import etree
import re

def _register_function(f):
    """ Register extension function with lxml """
    ns = etree.FunctionNamespace('http://wolnelektury.pl/functions')
    ns[f.__name__] = f


def reg_substitute_entities(): 
    ENTITY_SUBSTITUTIONS = [
        (u'---', u'—'),
        (u'--', u'–'),
        (u'...', u'…'),
        (u',,', u'„'),
        (u'"', u'”'),
    ]

    def substitute_entities(context, text):
        """XPath extension function converting all entites in passed text."""
        if isinstance(text, list):
            text = ''.join(text)
        for entity, substitutution in ENTITY_SUBSTITUTIONS:
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


def reg_wrap_words():
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
    _register_function(wrap_words)


def reg_person_name():
    def person_name(context, text):
        """ Converts "Name, Forename" to "Forename Name" """
        if isinstance(text, list):
            text = ''.join(text)
        return ' '.join([t.strip() for t in text.split(',', 1)[::-1]])
    _register_function(person_name)

