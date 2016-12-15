# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import re
import urllib
from .utils import XMLNamespace


class UnicodeException(Exception):
    def __str__(self):
        """ Dirty workaround for Python Unicode handling problems. """
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        """ Dirty workaround for Python Unicode handling problems. """
        args = self.args[0] if len(self.args) == 1 else self.args
        try:
            message = unicode(args)
        except UnicodeDecodeError:
            message = unicode(args, encoding='utf-8', errors='ignore')
        return message


class ParseError(UnicodeException):
    pass


class ValidationError(UnicodeException):
    pass


# was deleted, but still used???
class NoDublinCore(ValidationError):
    pass


class BuildError(Exception):
    pass


class EmptyNamespace(XMLNamespace):
    def __init__(self):
        super(EmptyNamespace, self).__init__('')

    def __call__(self, tag):
        return tag

# some common namespaces we use
RDFNS = XMLNamespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
DCNS = XMLNamespace('http://purl.org/dc/elements/1.1/')
XINS = XMLNamespace("http://www.w3.org/2001/XInclude")
XHTMLNS = XMLNamespace("http://www.w3.org/1999/xhtml")
NCXNS = XMLNamespace("http://www.daisy.org/z3986/2005/ncx/")
OPFNS = XMLNamespace("http://www.idpf.org/2007/opf")

SSTNS = XMLNamespace('http://nowoczesnapolska.org.pl/sst#')


class WLURI(object):
    """Represents a WL URI. Extracts slug from it."""
    slug = None

    example = 'http://wolnelektury.pl/katalog/lektura/template/'
    _re_wl_uri = re.compile(r'http://(www\.)?wolnelektury.pl/katalog/lektura/(?P<slug>[-a-z0-9]+)/?$')

    def __init__(self, uri):
        uri = unicode(uri)
        self.uri = uri
        self.slug = uri.rstrip('/').rsplit('/', 1)[-1]

    @classmethod
    def strict(cls, uri):
        match = cls._re_wl_uri.match(uri)
        if not match:
            raise ValidationError(u'Invalid URI (%s). Should match: %s' % (
                        uri, cls._re_wl_uri.pattern))
        return cls(uri)

    @classmethod
    def from_slug(cls, slug):
        """Contructs an URI from slug.

        >>> WLURI.from_slug('a-slug').uri
        u'http://wolnelektury.pl/katalog/lektura/a-slug/'

        """
        uri = 'http://wolnelektury.pl/katalog/lektura/%s/' % slug
        return cls(uri)

    def __unicode__(self):
        return self.uri

    def __str__(self):
        return self.uri

    def __eq__(self, other):
        return self.slug == other.slug


class URLOpener(urllib.FancyURLopener):
    version = 'FNP Librarian (http://git.nowoczesnapolska.org.pl/?p=librarian.git)'
urllib._urlopener = URLOpener()
