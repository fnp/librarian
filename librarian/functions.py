# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from lxml import etree
import re

from librarian.dcparser import Person

def _register_function(f):
    """ Register extension function with lxml """
    ns = etree.FunctionNamespace('http://wolnelektury.pl/functions')
    ns[f.__name__] = f


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


def reg_substitute_entities():
    _register_function(substitute_entities)


def strip(context, text):
    """Remove unneeded whitespace from beginning and end"""
    if isinstance(text, list):
        text = ''.join(text)
    return re.sub(r'\s+', ' ', text).strip()


def reg_strip():
    _register_function(strip)


def starts_white(context, text):
    if isinstance(text, list):
        text = ''.join(text)
    if not text:
        return False
    return text[0].isspace()


def reg_starts_white():
    _register_function(starts_white)


def reg_ends_white():
    def ends_white(context, text):
        if isinstance(text, list):
            text = ''.join(text)
        if not text:
            return False
        return text[-1].isspace()
    _register_function(ends_white)


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


def reg_wrap_words():
    _register_function(wrap_words)


def person_name(context, text):
    """ Converts "Name, Forename" to "Forename Name" """
    if isinstance(text, list):
        text = ''.join(text)
    return Person.from_text(text).readable()


def reg_person_name():
    _register_function(person_name)


def texcommand(context, text):
    """Remove non-letters"""
    if isinstance(text, list):
        text = ''.join(text)
    return re.sub(r'[^a-zA-Z]', '', text).strip()


def reg_texcommand():
    _register_function(texcommand)


def reg_get(format_):
    def get(context, *args):
        obj = format_
        for arg in args:
            if hasattr(obj, arg):
                obj = getattr(obj, arg)
            else:
                try:
                    obj = obj[arg]
                except (TypeError, KeyError), e:
                    # Just raise proper AttributeError.
                    getattr(obj, arg)
        return obj
    _register_function(get)
