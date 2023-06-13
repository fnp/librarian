# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from __future__ import print_function, unicode_literals

import os
import re
import shutil
from tempfile import NamedTemporaryFile
import urllib
from lxml import etree
import six
from six.moves.urllib.request import FancyURLopener
from .util import makedirs

# Compatibility imports.
from .meta.types.wluri import WLURI


@six.python_2_unicode_compatible
class UnicodeException(Exception):
    def __str__(self):
        """ Dirty workaround for Python Unicode handling problems. """
        args = self.args[0] if len(self.args) == 1 else self.args
        try:
            message = six.text_type(args)
        except UnicodeDecodeError:
            message = six.text_type(args, encoding='utf-8', errors='ignore')
        return message


class ParseError(UnicodeException):
    pass


class ValidationError(UnicodeException):
    pass


class NoDublinCore(ValidationError):
    """There's no DublinCore section, and it's required."""
    pass


class NoProvider(UnicodeException):
    """There's no DocProvider specified, and it's needed."""
    pass


class XMLNamespace(object):
    '''A handy structure to repsent names in an XML namespace.'''

    def __init__(self, uri):
        self.uri = uri

    def __call__(self, tag):
        return '{%s}%s' % (self.uri, tag)

    def __contains__(self, tag):
        return tag.startswith('{' + str(self) + '}')

    def __repr__(self):
        return 'XMLNamespace(%r)' % self.uri

    def __str__(self):
        return '%s' % self.uri


class EmptyNamespace(XMLNamespace):
    def __init__(self):
        super(EmptyNamespace, self).__init__('')

    def __call__(self, tag):
        return tag


# some common namespaces we use
XMLNS = XMLNamespace('http://www.w3.org/XML/1998/namespace')
RDFNS = XMLNamespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
DCNS = XMLNamespace('http://purl.org/dc/elements/1.1/')
XHTMLNS = XMLNamespace("http://www.w3.org/1999/xhtml")
PLMETNS = XMLNamespace("http://dl.psnc.pl/schemas/plmet/")

WLNS = EmptyNamespace()


class DocProvider(object):
    """Base class for a repository of XML files.

    Used for generating joined files, like EPUBs.
    """

    def by_slug(self, slug):
        """Should return a file-like object with a WL document XML."""
        raise NotImplementedError


class DirDocProvider(DocProvider):
    """ Serve docs from a directory of files in form <slug>.xml """

    def __init__(self, dir_):
        self.dir = dir_
        self.files = {}

    def by_slug(self, slug):
        fname = slug + '.xml'
        return open(os.path.join(self.dir, fname), 'rb')


def get_resource(path):
    return os.path.join(os.path.dirname(__file__), path)


class OutputFile(object):
    """Represents a file returned by one of the converters."""

    _bytes = None
    _filename = None

    def __del__(self):
        if self._filename:
            os.unlink(self._filename)

    def __nonzero__(self):
        return self._bytes is not None or self._filename is not None

    @classmethod
    def from_bytes(cls, bytestring):
        """Converter returns contents of a file as a string."""

        instance = cls()
        instance._bytes = bytestring
        return instance

    @classmethod
    def from_filename(cls, filename):
        """Converter returns contents of a file as a named file."""

        instance = cls()
        instance._filename = filename
        return instance

    def get_bytes(self):
        """Get file's contents as a bytestring."""

        if self._filename is not None:
            with open(self._filename, 'rb') as f:
                return f.read()
        else:
            return self._bytes

    def get_file(self):
        """Get file as a file-like object."""

        if self._bytes is not None:
            return six.BytesIO(self._bytes)
        elif self._filename is not None:
            return open(self._filename, 'rb')

    def get_filename(self):
        """Get file as a fs path."""

        if self._filename is not None:
            return self._filename
        elif self._bytes is not None:
            temp = NamedTemporaryFile(prefix='librarian-', delete=False)
            temp.write(self._bytes)
            temp.close()
            self._filename = temp.name
            return self._filename
        else:
            return None

    def save_as(self, path):
        """Save file to a path. Create directories, if necessary."""

        dirname = os.path.dirname(os.path.abspath(path))
        makedirs(dirname)
        shutil.copy(self.get_filename(), path)


class URLOpener(FancyURLopener):
    version = 'FNP Librarian (http://github.com/fnp/librarian)'


urllib._urlopener = URLOpener()
